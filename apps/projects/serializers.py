"""
Project serializers
"""
from rest_framework import serializers
from .models import Project, Unit, Stage, Block, Typology, Amenity, OrbitView


class AmenitySerializer(serializers.ModelSerializer):
    """Serializer for Amenity model"""
    
    class Meta:
        model = Amenity
        fields = '__all__'
        read_only_fields = ['id', 'company', 'created_at', 'updated_at', 'slug']


class TypologySerializer(serializers.ModelSerializer):
    """Serializer for Typology model"""
    units_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Typology
        fields = '__all__'
        read_only_fields = ['id', 'company', 'created_at', 'updated_at', 'slug']
    
    def get_units_count(self, obj):
        return obj.units.count()


class TypologyDetailSerializer(TypologySerializer):
    """Detailed serializer for Typology with media items"""
    pass


class UnitSerializer(serializers.ModelSerializer):
    """Serializer for Unit model"""
    project_name = serializers.CharField(source='project.name', read_only=True)
    block_name = serializers.CharField(source='block.name', read_only=True, allow_null=True)
    typology_data = TypologySerializer(source='typology', read_only=True, allow_null=True)
    
    class Meta:
        model = Unit
        fields = '__all__'
        read_only_fields = ['id', 'company', 'created_at', 'updated_at', 'price_per_sqm', 'slug']


class UnitListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for unit lists"""
    
    class Meta:
        model = Unit
        fields = [
            'id', 'name', 'code', 'unit_number', 'slug', 'status', 
            'floor', 'bedrooms', 'bathrooms', 'private_area', 'build_area',
            'price', 'fixed_price', 'price_type', 'currency', 'typology_slug',
            'glb_code'
        ]


class BlockSerializer(serializers.ModelSerializer):
    """Serializer for Block model"""
    stage_name = serializers.CharField(source='stage.name', read_only=True)
    amenities = serializers.SerializerMethodField()
    units = UnitListSerializer(many=True, read_only=True)
    units_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Block
        fields = '__all__'
        read_only_fields = ['id', 'company', 'created_at', 'updated_at', 'slug']
    
    def get_amenities(self, obj):
        amenities = Amenity.objects.filter(parent_type='block', parent_id=str(obj.id))
        return AmenitySerializer(amenities, many=True).data
    
    def get_units_count(self, obj):
        return obj.units.count()


class StageSerializer(serializers.ModelSerializer):
    """Serializer for Stage model"""
    project_name = serializers.CharField(source='project.name', read_only=True)
    blocks = BlockSerializer(many=True, read_only=True)
    typologies = TypologySerializer(many=True, read_only=True)
    blocks_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Stage
        fields = '__all__'
        read_only_fields = ['id', 'company', 'created_at', 'updated_at', 'slug']
    
    def get_blocks_count(self, obj):
        return obj.blocks.count()


class StageListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for stage lists"""
    blocks_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Stage
        fields = [
            'id', 'name', 'slug', 'code', 'stage_number', 'housing_typology',
            'separation', 'down_payment', 'discount', 'projected_increase',
            'closing_date', 'blocks_count'
        ]
    
    def get_blocks_count(self, obj):
        return obj.blocks.count()


class OrbitViewSerializer(serializers.ModelSerializer):
    """Serializer for OrbitView model"""
    project_name = serializers.CharField(source='project.name', read_only=True)
    
    class Meta:
        model = OrbitView
        fields = '__all__'
        read_only_fields = ['id', 'company', 'created_at', 'updated_at']


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project model"""
    stages = StageListSerializer(many=True, read_only=True)
    orbit_views_data = OrbitViewSerializer(source='orbit_views', many=True, read_only=True)
    occupancy_rate = serializers.FloatField(read_only=True)
    project_manager_name = serializers.CharField(source='project_manager.full_name', read_only=True, allow_null=True)
    
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['id', 'company', 'created_at', 'updated_at', 'view_count', 'lead_count', 'quote_count', 'slug']


class ProjectDetailSerializer(ProjectSerializer):
    """Detailed serializer for Project with full nested data"""
    stages = StageSerializer(many=True, read_only=True)


class ProjectListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for project lists"""
    occupancy_rate = serializers.FloatField(read_only=True)
    available_units_count = serializers.IntegerField(source='available_units', read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'code', 'slug', 'type', 'status', 'city', 'state', 'country',
            'total_units', 'available_units', 'available_units_count',
            'price_from', 'price_to', 'currency', 'measure_unit',
            'main_image', 'featured', 'occupancy_rate', 'background_color', 
            'accent_color', 'created_at'
        ]

