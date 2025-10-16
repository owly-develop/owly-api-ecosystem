"""
Project views
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Avg, Count, Sum
from apps.core.permissions import IsTenantUser
from .models import Project, Unit
from .serializers import ProjectSerializer, ProjectListSerializer, UnitSerializer
from .filters import ProjectFilter, UnitFilter


class ProjectViewSet(viewsets.ModelViewSet):
    """ViewSet for managing projects"""
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated, IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProjectFilter
    search_fields = ['name', 'code', 'description', 'city', 'state', 'address']
    ordering_fields = ['created_at', 'name', 'price_from', 'total_units', 'available_units']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Project.objects.all()
        if hasattr(user, 'company'):
            return Project.objects.filter(company=user.company, is_deleted=False)
        return Project.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)
    
    @action(detail=True, methods=['get'])
    def units(self, request, pk=None):
        """Get all units for a project"""
        project = self.get_object()
        units = project.units.filter(is_deleted=False)
        serializer = UnitSerializer(units, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get project statistics"""
        project = self.get_object()
        
        units = project.units.filter(is_deleted=False)
        
        stats = {
            'total_units': project.total_units,
            'available_units': project.available_units,
            'sold_units': project.sold_units,
            'reserved_units': project.reserved_units,
            'occupancy_rate': project.occupancy_rate,
            'lead_count': project.lead_count,
            'quote_count': project.quote_count,
            'view_count': project.view_count,
            'avg_unit_price': units.aggregate(avg=Avg('price'))['avg'] or 0,
            'avg_unit_area': units.aggregate(avg=Avg('area_sqm'))['avg'] or 0,
            'units_by_type': dict(units.values('unit_type').annotate(count=Count('id')).values_list('unit_type', 'count')),
            'units_by_floor': dict(units.values('floor').annotate(count=Count('id')).values_list('floor', 'count')),
        }
        return Response(stats)
    
    @action(detail=True, methods=['get'])
    def available_units(self, request, pk=None):
        """Get all available units for a project"""
        project = self.get_object()
        units = project.units.filter(is_deleted=False, status='available').order_by('floor', 'unit_number')
        serializer = UnitSerializer(units, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured projects"""
        projects = self.get_queryset().filter(featured=True, status='active')
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_location(self, request):
        """Get projects grouped by location"""
        queryset = self.get_queryset()
        
        # Group by city
        by_city = {}
        cities = queryset.values('city', 'state').distinct()
        
        for location in cities:
            city = location['city']
            state = location['state']
            key = f"{city}, {state}"
            
            city_projects = queryset.filter(city=city, state=state)
            by_city[key] = {
                'count': city_projects.count(),
                'total_units': city_projects.aggregate(total=Sum('total_units'))['total'] or 0,
                'available_units': city_projects.aggregate(total=Sum('available_units'))['total'] or 0,
                'projects': ProjectListSerializer(city_projects[:10], many=True).data
            }
        
        return Response(by_city)


class UnitViewSet(viewsets.ModelViewSet):
    """ViewSet for managing units"""
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated, IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = UnitFilter
    search_fields = ['unit_number', 'unit_type', 'orientation', 'view_type']
    ordering_fields = ['floor', 'unit_number', 'price', 'area_sqm', 'bedrooms']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Unit.objects.all()
        if hasattr(user, 'company'):
            return Unit.objects.filter(company=user.company, is_deleted=False)
        return Unit.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)
    
    @action(detail=True, methods=['post'])
    def reserve(self, request, pk=None):
        """Reserve a unit for a lead"""
        unit = self.get_object()
        lead_id = request.data.get('lead_id')
        
        if unit.status != 'available':
            return Response(
                {'error': 'Unit is not available'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not lead_id:
            return Response(
                {'error': 'lead_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from apps.leads.models import Lead
        from django.utils import timezone
        
        try:
            lead = Lead.objects.get(id=lead_id, company=request.user.company)
            unit.status = 'reserved'
            unit.reserved_by = lead
            unit.reserved_date = timezone.now()
            unit.save()
            
            # Update project counts
            project = unit.project
            project.available_units -= 1
            project.reserved_units += 1
            project.save()
            
            serializer = self.get_serializer(unit)
            return Response(serializer.data)
        except Lead.DoesNotExist:
            return Response(
                {'error': 'Lead not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def mark_as_sold(self, request, pk=None):
        """Mark unit as sold"""
        unit = self.get_object()
        sold_to = request.data.get('sold_to')
        
        from django.utils import timezone
        
        unit.status = 'sold'
        unit.sold_to = sold_to
        unit.sold_date = timezone.now()
        unit.save()
        
        # Update project counts
        project = unit.project
        if unit.status == 'reserved':
            project.reserved_units -= 1
        else:
            project.available_units -= 1
        project.sold_units += 1
        project.save()
        
        serializer = self.get_serializer(unit)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def similar(self, request):
        """Find similar units based on criteria"""
        unit_type = request.query_params.get('unit_type')
        bedrooms = request.query_params.get('bedrooms')
        price_range = request.query_params.get('price_range', 10)  # % range
        
        queryset = self.get_queryset().filter(status='available')
        
        if unit_type:
            queryset = queryset.filter(unit_type=unit_type)
        
        if bedrooms:
            queryset = queryset.filter(bedrooms=int(bedrooms))
        
        serializer = self.get_serializer(queryset[:20], many=True)
        return Response(serializer.data)

