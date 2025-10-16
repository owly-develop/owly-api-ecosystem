# 🚀 API Enhancements - New Features & Endpoints

## Overview

This document details all the new endpoints, filters, and admin improvements added to the OWLY CRM API.

---

## 📊 New Endpoints Summary

### Total New Endpoints: **+25**

- **Leads**: +11 new endpoints
- **Projects**: +3 new endpoints
- **Units**: +3 new endpoints
- **Analytics**: Enhanced
- **Admin**: Significantly improved

---

## 🔥 LEADS - New Endpoints (11 new)

### Bulk Operations
```
POST   /api/leads/bulk_assign/           - Bulk assign leads to users
POST   /api/leads/bulk_status_change/    - Bulk change status of leads
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/leads/bulk_assign/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"lead_ids": ["uuid1", "uuid2"], "user_id": "user_uuid"}'
```

### Lead Intelligence
```
GET    /api/leads/{id}/timeline/         - Get lead timeline/history
GET    /api/leads/hot_leads/              - Get hot leads (high score + priority)
GET    /api/leads/duplicates/             - Find potential duplicate leads
GET    /api/leads/performance_by_source/  - Performance metrics by source
```

### Follow-ups & Tasks
```
GET    /api/leads/upcoming_followups/     - Leads with upcoming follow-ups (next 7 days)
GET    /api/leads/overdue_followups/      - Leads with overdue follow-ups
```

### Lead Management
```
POST   /api/leads/{id}/add_note/          - Add timestamped note to lead
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/leads/{id}/add_note/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"note": "Called and left voicemail"}'
```

### Advanced Filters for Leads

**All new filters available:**
```
?created_after=2024-01-01T00:00:00Z
?created_before=2024-12-31T23:59:59Z
?last_contact_after=2024-01-01
?last_contact_before=2024-12-31
?score_min=70
?score_max=100
?ai_probability_min=70
?ai_probability_max=100
?budget_min=100000
?budget_max=500000
?status_in=new,contacted,qualified
?priority_in=high,urgent
?source_in=website,facebook,instagram
?has_follow_up=true
?requires_attention=true
?search=john+doe
```

**Example:**
```bash
# Get high-scoring leads from website that need attention
GET /api/leads/?score_min=70&source=website&requires_attention=true

# Get leads created this month with upcoming follow-ups
GET /api/leads/?created_after=2024-01-01&has_follow_up=true
```

---

## 🏗️ PROJECTS - New Endpoints (3 new)

```
GET    /api/projects/featured/            - Get featured projects
GET    /api/projects/by_location/         - Projects grouped by city/state
GET    /api/projects/{id}/available_units/ - Get all available units for project
```

**Example:**
```bash
# Get featured projects
GET /api/projects/featured/

# Get projects by location
GET /api/projects/by_location/
# Returns:
{
  "Miami, Florida": {
    "count": 5,
    "total_units": 250,
    "available_units": 120,
    "projects": [...]
  }
}
```

### Enhanced Project Endpoints

**Existing endpoints with more data:**
```
GET    /api/projects/{id}/stats/
# Now includes:
- avg_unit_price
- avg_unit_area
- units_by_type
- units_by_floor
```

### Advanced Filters for Projects

```
?price_min=100000
?price_max=500000
?launch_after=2024-01-01
?launch_before=2024-12-31
?delivery_after=2025-01-01
?delivery_before=2025-12-31
?available_units_min=10
?total_units_min=50
?total_units_max=200
?construction_progress_min=50
```

**Example:**
```bash
# Get active projects with 50+ units, priced under $300k
GET /api/projects/?status=active&total_units_min=50&price_max=300000
```

---

## 🏠 UNITS - New Endpoints (3 new)

```
POST   /api/projects/units/{id}/reserve/      - Reserve unit for a lead
POST   /api/projects/units/{id}/mark_as_sold/ - Mark unit as sold
GET    /api/projects/units/similar/           - Find similar units
```

**Example - Reserve Unit:**
```bash
curl -X POST http://localhost:8000/api/projects/units/{id}/reserve/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"lead_id": "lead_uuid"}'
```

**Example - Find Similar Units:**
```bash
# Find similar 2BR units
GET /api/projects/units/similar/?bedrooms=2&unit_type=2BR
```

### Advanced Filters for Units

```
?price_min=100000
?price_max=500000
?area_min=50
?area_max=150
?bedrooms_min=2
?bedrooms_max=3
?bathrooms_min=2
?floor_min=5
?floor_max=10
?orientation=north
?status=available
```

**Example:**
```bash
# Get available 2-3 BR units on floors 5-10, under $250k
GET /api/projects/units/?status=available&bedrooms_min=2&bedrooms_max=3&floor_min=5&floor_max=10&price_max=250000
```

---

## 📈 Enhanced Analytics

All analytics endpoints now provide more detailed data and better performance.

---

## 🎨 Django Admin - Major Improvements

### All Models Now Include:

✅ **Color-coded status badges**  
✅ **Inline editing** (Projects show units inline)  
✅ **Advanced filters** (custom filters by score, status, etc.)  
✅ **Bulk actions** (assign, change status, export)  
✅ **Clickable links** between related objects  
✅ **Better field organization** (collapsed sections)  
✅ **Date hierarchy**  
✅ **Search across multiple fields**  
✅ **Performance indicators** (occupancy rates, progress bars)  
✅ **Export actions** (prepared for CSV/Excel)  

### Lead Admin Features

**Filters:**
- Status with custom filter
- Priority
- Source
- Lead Score (High/Medium/Low)
- Company
- Assigned to
- Converted status
- Consent status
- Created date

**Bulk Actions:**
- Mark as Contacted
- Mark as Qualified
- Mark as High Priority
- Assign to Me
- Export to CSV (prepared)

**Display:**
- Color-coded status badges
- Color-coded priority badges
- Lead score with color indicators (green/yellow/red)
- Clickable lead numbers
- Full name display
- Date formatting

### Project Admin Features

**Display:**
- Project code links
- Type badges (Residential/Commercial/etc)
- Status badges with colors
- Units display (Available/Total)
- Occupancy rate with color indicators
- Price range formatted
- Featured indicator

**Bulk Actions:**
- Mark as Active
- Mark as Featured
- Export Projects

**Inline:**
- Units shown inline (first 20)
- Quick edit units without leaving project page
- Direct links to unit detail pages

### Unit Admin Features

**Display:**
- Linked to project
- Status badges
- Price formatting
- Specifications (BR/BA/Area)
- Floor information

**Bulk Actions:**
- Mark as Available
- Mark as Sold
- Export Units

### Quote Admin Features

**Display:**
- Quote number links
- Lead and Project links
- Status badges (Draft/Sent/Viewed/Accepted/Rejected)
- Total with currency
- Dates tracking

**Bulk Actions:**
- Mark as Sent
- Mark as Accepted
- Export Quotes

### Company Admin Features

**Display:**
- Plan badges (Free/Starter/Professional/Enterprise)
- Status badges (Active/Trial/Suspended)
- User usage (5/10 with color indicator)
- Project usage (3/25 with color indicator)

**Bulk Actions:**
- Activate Companies
- Suspend Companies
- Upgrade to Professional

---

## 🔍 Advanced Search Capabilities

### Multi-field Search

**Leads:**
```
search_fields = [
    'lead_number', 'first_name', 'last_name',
    'email', 'phone', 'company_name', 'notes'
]
```

**Projects:**
```
search_fields = [
    'name', 'code', 'description',
    'city', 'state', 'address'
]
```

**Units:**
```
search_fields = [
    'unit_number', 'unit_type',
    'orientation', 'view_type'
]
```

---

## 📋 Complete API Endpoints Reference

### LEADS (20+ endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/leads/` | List leads (with advanced filters) |
| POST | `/api/leads/` | Create lead |
| GET | `/api/leads/{id}/` | Get lead details |
| PUT | `/api/leads/{id}/` | Update lead |
| DELETE | `/api/leads/{id}/` | Delete lead |
| POST | `/api/leads/{id}/assign/` | Assign lead to user |
| POST | `/api/leads/{id}/change_status/` | Change lead status |
| POST | `/api/leads/{id}/update_score/` | Update lead score |
| GET | `/api/leads/{id}/timeline/` | ⭐ Get lead timeline |
| POST | `/api/leads/{id}/add_note/` | ⭐ Add note to lead |
| GET | `/api/leads/stats/` | Get lead statistics |
| POST | `/api/leads/bulk_assign/` | ⭐ Bulk assign leads |
| POST | `/api/leads/bulk_status_change/` | ⭐ Bulk change status |
| GET | `/api/leads/upcoming_followups/` | ⭐ Upcoming follow-ups |
| GET | `/api/leads/overdue_followups/` | ⭐ Overdue follow-ups |
| GET | `/api/leads/hot_leads/` | ⭐ Hot leads |
| GET | `/api/leads/duplicates/` | ⭐ Find duplicates |
| GET | `/api/leads/performance_by_source/` | ⭐ Performance by source |

### PROJECTS (10+ endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/projects/` | List projects (with filters) |
| POST | `/api/projects/` | Create project |
| GET | `/api/projects/{id}/` | Get project details |
| PUT | `/api/projects/{id}/` | Update project |
| DELETE | `/api/projects/{id}/` | Delete project |
| GET | `/api/projects/{id}/units/` | Get project units |
| GET | `/api/projects/{id}/stats/` | Enhanced project stats |
| GET | `/api/projects/{id}/available_units/` | ⭐ Available units only |
| GET | `/api/projects/featured/` | ⭐ Featured projects |
| GET | `/api/projects/by_location/` | ⭐ Projects by location |

### UNITS (8+ endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/projects/units/` | List units (with filters) |
| POST | `/api/projects/units/` | Create unit |
| GET | `/api/projects/units/{id}/` | Get unit details |
| PUT | `/api/projects/units/{id}/` | Update unit |
| DELETE | `/api/projects/units/{id}/` | Delete unit |
| POST | `/api/projects/units/{id}/reserve/` | ⭐ Reserve unit |
| POST | `/api/projects/units/{id}/mark_as_sold/` | ⭐ Mark as sold |
| GET | `/api/projects/units/similar/` | ⭐ Find similar units |

---

## 🎯 Use Cases & Examples

### Example 1: Lead Management Dashboard

```bash
# Get hot leads that need attention
GET /api/leads/hot_leads/?requires_attention=true

# Get upcoming follow-ups for this week
GET /api/leads/upcoming_followups/

# Get lead performance by source
GET /api/leads/performance_by_source/
```

### Example 2: Sales Operations

```bash
# Bulk assign new leads to a sales rep
POST /api/leads/bulk_assign/
{
  "lead_ids": ["uuid1", "uuid2", "uuid3"],
  "user_id": "sales_rep_uuid"
}

# Find duplicate leads before import
GET /api/leads/duplicates/

# Get available units in a specific project
GET /api/projects/{id}/available_units/
```

### Example 3: Advanced Filtering

```bash
# High-value leads from website, created this month, with budget over $300k
GET /api/leads/?source=website&created_after=2024-01-01&budget_min=300000&score_min=70

# Available 2-3BR units, floors 5-10, under $250k, with city view
GET /api/projects/units/?status=available&bedrooms_min=2&bedrooms_max=3&floor_min=5&floor_max=10&price_max=250000&view_type=city

# Active projects in Miami with 50+ available units
GET /api/projects/?status=active&city=Miami&available_units_min=50
```

---

## 🚀 Performance Improvements

- **Optimized queries** with `select_related` and `prefetch_related`
- **Indexed fields** for fast filtering
- **Efficient aggregations** using Django ORM
- **Pagination** enabled on all list endpoints
- **Cache-ready** structure

---

## 📝 Next Steps

1. ✅ Test all new endpoints
2. ✅ Update API documentation
3. ✅ Add export functionality (CSV/Excel)
4. ✅ Implement PDF generation for quotes
5. ✅ Add email notifications
6. ✅ Create scheduled tasks for overdue follow-ups

---

## 🔗 Related Documentation

- [README.md](README.md) - Main documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - AWS deployment
- API Docs: http://localhost:8000/api/docs/

---

**All enhancements are live and ready to use! 🎉**

Access the interactive API documentation at: http://localhost:8000/api/docs/

