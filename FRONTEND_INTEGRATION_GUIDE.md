# 🔌 Guía de Integración Frontend → API

## 🎯 Objetivo

Conectar tu frontend React existente (`owly-crm/src`) con la API Django (`owly-api-django`).

---

## 📋 Visión General

```
┌─────────────────────────┐         ┌─────────────────────────┐
│   FRONTEND REACT        │  HTTP   │   DJANGO API            │
│   localhost:5173        │ ◄────► │   localhost:8000        │
│                         │  JWT    │                         │
│   • TypeScript          │         │   • Django REST         │
│   • React Router        │         │   • PostgreSQL          │
│   • Zustand/Redux       │         │   • JWT Auth            │
│   • Axios/Fetch         │         │   • Multi-tenant        │
└─────────────────────────┘         └─────────────────────────┘
```

---

## 🔧 PASO 1: Configurar CORS en la API

### 1.1 Actualizar archivo `.env` de la API

```bash
# En owly-api-django/.env
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000,http://localhost:5174
```

**Por qué**: El frontend corre en puerto diferente al backend, necesitas habilitar CORS.

### 1.2 Verificar settings.py

Ya está configurado en `owly_crm/settings.py`:
```python
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:5173,http://localhost:3000',
    cast=Csv()
)
CORS_ALLOW_CREDENTIALS = True
```

### 1.3 Reiniciar API

```bash
cd owly-api-django
docker-compose restart web
```

---

## 🔧 PASO 2: Configurar el Frontend

### 2.1 Crear archivo de configuración API

**Crear**: `src/config/api.ts`

```typescript
// src/config/api.ts

// URL base de la API
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Endpoints
export const API_ENDPOINTS = {
  // Authentication
  auth: {
    login: `${API_BASE_URL}/auth/login/`,
    refresh: `${API_BASE_URL}/auth/refresh/`,
    verify: `${API_BASE_URL}/auth/verify/`,
    profile: `${API_BASE_URL}/auth/users/profile/`,
    changePassword: `${API_BASE_URL}/auth/users/change_password/`,
  },
  
  // Companies
  companies: {
    list: `${API_BASE_URL}/companies/`,
    detail: (id: string) => `${API_BASE_URL}/companies/${id}/`,
    stats: (id: string) => `${API_BASE_URL}/companies/${id}/stats/`,
  },
  
  // Projects
  projects: {
    list: `${API_BASE_URL}/projects/`,
    detail: (id: string) => `${API_BASE_URL}/projects/${id}/`,
    units: (id: string) => `${API_BASE_URL}/projects/${id}/units/`,
    availableUnits: (id: string) => `${API_BASE_URL}/projects/${id}/available_units/`,
    stats: (id: string) => `${API_BASE_URL}/projects/${id}/stats/`,
    featured: `${API_BASE_URL}/projects/featured/`,
    byLocation: `${API_BASE_URL}/projects/by_location/`,
  },
  
  // Units
  units: {
    list: `${API_BASE_URL}/projects/units/`,
    detail: (id: string) => `${API_BASE_URL}/projects/units/${id}/`,
    reserve: (id: string) => `${API_BASE_URL}/projects/units/${id}/reserve/`,
    markAsSold: (id: string) => `${API_BASE_URL}/projects/units/${id}/mark_as_sold/`,
    similar: `${API_BASE_URL}/projects/units/similar/`,
  },
  
  // Leads
  leads: {
    list: `${API_BASE_URL}/leads/`,
    detail: (id: string) => `${API_BASE_URL}/leads/${id}/`,
    assign: (id: string) => `${API_BASE_URL}/leads/${id}/assign/`,
    changeStatus: (id: string) => `${API_BASE_URL}/leads/${id}/change_status/`,
    updateScore: (id: string) => `${API_BASE_URL}/leads/${id}/update_score/`,
    timeline: (id: string) => `${API_BASE_URL}/leads/${id}/timeline/`,
    addNote: (id: string) => `${API_BASE_URL}/leads/${id}/add_note/`,
    bulkAssign: `${API_BASE_URL}/leads/bulk_assign/`,
    bulkStatusChange: `${API_BASE_URL}/leads/bulk_status_change/`,
    hotLeads: `${API_BASE_URL}/leads/hot_leads/`,
    duplicates: `${API_BASE_URL}/leads/duplicates/`,
    upcomingFollowups: `${API_BASE_URL}/leads/upcoming_followups/`,
    overdueFollowups: `${API_BASE_URL}/leads/overdue_followups/`,
    performanceBySource: `${API_BASE_URL}/leads/performance_by_source/`,
    stats: `${API_BASE_URL}/leads/stats/`,
  },
  
  // Quotes
  quotes: {
    list: `${API_BASE_URL}/quotes/`,
    detail: (id: string) => `${API_BASE_URL}/quotes/${id}/`,
    send: (id: string) => `${API_BASE_URL}/quotes/${id}/send/`,
    accept: (id: string) => `${API_BASE_URL}/quotes/${id}/accept/`,
    reject: (id: string) => `${API_BASE_URL}/quotes/${id}/reject/`,
    markViewed: (id: string) => `${API_BASE_URL}/quotes/${id}/mark_viewed/`,
  },
  
  // Analytics
  analytics: {
    dashboard: `${API_BASE_URL}/analytics/dashboard/`,
    salesFunnel: `${API_BASE_URL}/analytics/sales-funnel/`,
    leadAnalytics: `${API_BASE_URL}/analytics/leads/`,
  },
  
  // Activities
  activities: {
    list: `${API_BASE_URL}/activities/`,
    detail: (id: string) => `${API_BASE_URL}/activities/${id}/`,
  },
};
```

### 2.2 Crear archivo `.env` en el frontend

**Crear**: `.env` en la raíz del proyecto frontend

```bash
# owly-crm/.env
VITE_API_URL=http://localhost:8000/api
```

---

## 🔐 PASO 3: Implementar Servicio de Autenticación

### 3.1 Crear servicio de autenticación

**Crear**: `src/services/auth.service.ts`

```typescript
// src/services/auth.service.ts
import { API_ENDPOINTS } from '@/config/api';

interface LoginCredentials {
  email: string;
  password: string;
}

interface TokenResponse {
  access: string;
  refresh: string;
}

interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  role: 'admin' | 'manager' | 'sales' | 'marketing' | 'support';
  company: string;
  company_name: string;
}

class AuthService {
  private accessToken: string | null = null;
  private refreshToken: string | null = null;

  /**
   * Login user and store tokens
   */
  async login(credentials: LoginCredentials): Promise<TokenResponse> {
    const response = await fetch(API_ENDPOINTS.auth.login, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Login failed');
    }

    const tokens: TokenResponse = await response.json();
    
    // Guardar tokens
    this.setTokens(tokens.access, tokens.refresh);
    
    return tokens;
  }

  /**
   * Logout user
   */
  logout(): void {
    this.clearTokens();
    // Redirigir a login
    window.location.href = '/login';
  }

  /**
   * Get access token
   */
  getAccessToken(): string | null {
    if (!this.accessToken) {
      this.accessToken = localStorage.getItem('access_token');
    }
    return this.accessToken;
  }

  /**
   * Get refresh token
   */
  getRefreshToken(): string | null {
    if (!this.refreshToken) {
      this.refreshToken = localStorage.getItem('refresh_token');
    }
    return this.refreshToken;
  }

  /**
   * Set tokens in memory and localStorage
   */
  private setTokens(access: string, refresh: string): void {
    this.accessToken = access;
    this.refreshToken = refresh;
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
  }

  /**
   * Clear tokens
   */
  private clearTokens(): void {
    this.accessToken = null;
    this.refreshToken = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  }

  /**
   * Refresh access token
   */
  async refreshAccessToken(): Promise<string> {
    const refreshToken = this.getRefreshToken();
    
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await fetch(API_ENDPOINTS.auth.refresh, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh: refreshToken }),
    });

    if (!response.ok) {
      this.logout();
      throw new Error('Token refresh failed');
    }

    const data = await response.json();
    this.setTokens(data.access, data.refresh);
    
    return data.access;
  }

  /**
   * Get current user profile
   */
  async getCurrentUser(): Promise<User> {
    const cachedUser = localStorage.getItem('user');
    if (cachedUser) {
      return JSON.parse(cachedUser);
    }

    const response = await this.makeAuthenticatedRequest(
      API_ENDPOINTS.auth.profile,
      { method: 'GET' }
    );

    const user = await response.json();
    localStorage.setItem('user', JSON.stringify(user));
    
    return user;
  }

  /**
   * Make authenticated request with automatic token refresh
   */
  async makeAuthenticatedRequest(
    url: string,
    options: RequestInit = {}
  ): Promise<Response> {
    const token = this.getAccessToken();

    if (!token) {
      throw new Error('No access token available');
    }

    // Add authorization header
    const headers = {
      ...options.headers,
      'Authorization': `Bearer ${token}`,
    };

    let response = await fetch(url, { ...options, headers });

    // If token expired (401), refresh and retry
    if (response.status === 401) {
      try {
        const newToken = await this.refreshAccessToken();
        
        // Retry with new token
        headers['Authorization'] = `Bearer ${newToken}`;
        response = await fetch(url, { ...options, headers });
      } catch (error) {
        this.logout();
        throw error;
      }
    }

    return response;
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return !!this.getAccessToken();
  }
}

// Export singleton instance
export const authService = new AuthService();
```

### 3.2 Crear hook de autenticación

**Crear**: `src/hooks/useAuth.ts`

```typescript
// src/hooks/useAuth.ts
import { useState, useEffect } from 'react';
import { authService } from '@/services/auth.service';

interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  role: string;
  company: string;
  company_name: string;
}

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  async function checkAuth() {
    try {
      if (authService.isAuthenticated()) {
        const currentUser = await authService.getCurrentUser();
        setUser(currentUser);
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      setUser(null);
    } finally {
      setLoading(false);
    }
  }

  async function login(email: string, password: string) {
    try {
      await authService.login({ email, password });
      const currentUser = await authService.getCurrentUser();
      setUser(currentUser);
      return { success: true };
    } catch (error: any) {
      return { success: false, error: error.message };
    }
  }

  function logout() {
    authService.logout();
    setUser(null);
  }

  return {
    user,
    loading,
    login,
    logout,
    isAuthenticated: !!user,
    isAdmin: user?.role === 'admin',
    isManager: user?.role === 'manager' || user?.role === 'admin',
  };
}
```

---

## 🔧 PASO 4: Crear Cliente API Genérico

### 4.1 Cliente API con tipos

**Crear**: `src/services/api.client.ts`

```typescript
// src/services/api.client.ts
import { authService } from './auth.service';

export interface ApiResponse<T> {
  count?: number;
  next?: string | null;
  previous?: string | null;
  results?: T[];
  data?: T;
}

export class ApiClient {
  /**
   * GET request
   */
  async get<T>(url: string, params?: Record<string, any>): Promise<T> {
    const queryString = params ? '?' + new URLSearchParams(params).toString() : '';
    const fullUrl = `${url}${queryString}`;

    const response = await authService.makeAuthenticatedRequest(fullUrl, {
      method: 'GET',
    });

    if (!response.ok) {
      throw await this.handleError(response);
    }

    return response.json();
  }

  /**
   * POST request
   */
  async post<T>(url: string, data: any): Promise<T> {
    const response = await authService.makeAuthenticatedRequest(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw await this.handleError(response);
    }

    return response.json();
  }

  /**
   * PUT request
   */
  async put<T>(url: string, data: any): Promise<T> {
    const response = await authService.makeAuthenticatedRequest(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw await this.handleError(response);
    }

    return response.json();
  }

  /**
   * PATCH request
   */
  async patch<T>(url: string, data: any): Promise<T> {
    const response = await authService.makeAuthenticatedRequest(url, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw await this.handleError(response);
    }

    return response.json();
  }

  /**
   * DELETE request
   */
  async delete<T>(url: string): Promise<T> {
    const response = await authService.makeAuthenticatedRequest(url, {
      method: 'DELETE',
    });

    if (!response.ok) {
      throw await this.handleError(response);
    }

    // DELETE might return empty response
    const text = await response.text();
    return text ? JSON.parse(text) : null;
  }

  /**
   * Handle API errors
   */
  private async handleError(response: Response): Promise<Error> {
    let errorMessage = 'API request failed';
    
    try {
      const errorData = await response.json();
      
      if (errorData.error && typeof errorData.error === 'object') {
        errorMessage = JSON.stringify(errorData.error);
      } else if (errorData.message) {
        errorMessage = errorData.message;
      } else if (errorData.detail) {
        errorMessage = errorData.detail;
      }
    } catch (e) {
      errorMessage = `HTTP ${response.status}: ${response.statusText}`;
    }

    return new Error(errorMessage);
  }
}

// Export singleton
export const apiClient = new ApiClient();
```

---

## 🔧 PASO 5: Crear Servicios por Modelo

### 5.1 Servicio de Leads

**Crear**: `src/services/leads.service.ts`

```typescript
// src/services/leads.service.ts
import { apiClient, ApiResponse } from './api.client';
import { API_ENDPOINTS } from '@/config/api';
import type { Lead, LeadFormData } from '@/types/lead';

export class LeadsService {
  /**
   * Get all leads with filters
   */
  async getLeads(filters?: {
    status?: string;
    priority?: string;
    source?: string;
    score_min?: number;
    score_max?: number;
    search?: string;
    page?: number;
  }): Promise<ApiResponse<Lead>> {
    return apiClient.get<ApiResponse<Lead>>(
      API_ENDPOINTS.leads.list,
      filters
    );
  }

  /**
   * Get single lead
   */
  async getLead(id: string): Promise<Lead> {
    return apiClient.get<Lead>(API_ENDPOINTS.leads.detail(id));
  }

  /**
   * Create new lead
   */
  async createLead(data: LeadFormData): Promise<Lead> {
    return apiClient.post<Lead>(API_ENDPOINTS.leads.list, data);
  }

  /**
   * Update lead
   */
  async updateLead(id: string, data: Partial<LeadFormData>): Promise<Lead> {
    return apiClient.patch<Lead>(API_ENDPOINTS.leads.detail(id), data);
  }

  /**
   * Delete lead
   */
  async deleteLead(id: string): Promise<void> {
    return apiClient.delete(API_ENDPOINTS.leads.detail(id));
  }

  /**
   * Assign lead to user
   */
  async assignLead(leadId: string, userId: string): Promise<Lead> {
    return apiClient.post<Lead>(
      API_ENDPOINTS.leads.assign(leadId),
      { user_id: userId }
    );
  }

  /**
   * Change lead status
   */
  async changeStatus(leadId: string, status: string): Promise<Lead> {
    return apiClient.post<Lead>(
      API_ENDPOINTS.leads.changeStatus(leadId),
      { status }
    );
  }

  /**
   * Add note to lead
   */
  async addNote(leadId: string, note: string): Promise<Lead> {
    return apiClient.post<Lead>(
      API_ENDPOINTS.leads.addNote(leadId),
      { note }
    );
  }

  /**
   * Get lead timeline
   */
  async getTimeline(leadId: string): Promise<any[]> {
    return apiClient.get<any[]>(API_ENDPOINTS.leads.timeline(leadId));
  }

  /**
   * Get hot leads
   */
  async getHotLeads(): Promise<Lead[]> {
    return apiClient.get<Lead[]>(API_ENDPOINTS.leads.hotLeads);
  }

  /**
   * Get upcoming follow-ups
   */
  async getUpcomingFollowups(): Promise<Lead[]> {
    return apiClient.get<Lead[]>(API_ENDPOINTS.leads.upcomingFollowups);
  }

  /**
   * Bulk assign leads
   */
  async bulkAssign(leadIds: string[], userId: string): Promise<any> {
    return apiClient.post(API_ENDPOINTS.leads.bulkAssign, {
      lead_ids: leadIds,
      user_id: userId,
    });
  }

  /**
   * Get lead statistics
   */
  async getStats(): Promise<any> {
    return apiClient.get(API_ENDPOINTS.leads.stats);
  }
}

export const leadsService = new LeadsService();
```

### 5.2 Servicio de Projects

**Crear**: `src/services/projects.service.ts`

```typescript
// src/services/projects.service.ts
import { apiClient, ApiResponse } from './api.client';
import { API_ENDPOINTS } from '@/config/api';
import type { Project } from '@/types/project';

export class ProjectsService {
  /**
   * Get all projects
   */
  async getProjects(filters?: {
    status?: string;
    type?: string;
    city?: string;
    featured?: boolean;
    price_min?: number;
    price_max?: number;
  }): Promise<ApiResponse<Project>> {
    return apiClient.get<ApiResponse<Project>>(
      API_ENDPOINTS.projects.list,
      filters
    );
  }

  /**
   * Get single project
   */
  async getProject(id: string): Promise<Project> {
    return apiClient.get<Project>(API_ENDPOINTS.projects.detail(id));
  }

  /**
   * Get project statistics
   */
  async getProjectStats(id: string): Promise<any> {
    return apiClient.get(API_ENDPOINTS.projects.stats(id));
  }

  /**
   * Get available units for project
   */
  async getAvailableUnits(id: string): Promise<any[]> {
    return apiClient.get(API_ENDPOINTS.projects.availableUnits(id));
  }

  /**
   * Get featured projects
   */
  async getFeaturedProjects(): Promise<Project[]> {
    return apiClient.get<Project[]>(API_ENDPOINTS.projects.featured);
  }
}

export const projectsService = new ProjectsService();
```

---

## 🎨 PASO 6: Crear Hook Genérico para Data Fetching

### 6.1 Hook useApi

**Crear**: `src/hooks/useApi.ts`

```typescript
// src/hooks/useApi.ts
import { useState, useEffect } from 'react';

interface UseApiOptions<T> {
  immediate?: boolean;
  onSuccess?: (data: T) => void;
  onError?: (error: Error) => void;
}

export function useApi<T>(
  apiFunction: () => Promise<T>,
  options: UseApiOptions<T> = {}
) {
  const { immediate = true, onSuccess, onError } = options;
  
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(immediate);
  const [error, setError] = useState<Error | null>(null);

  const execute = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const result = await apiFunction();
      setData(result);
      
      if (onSuccess) {
        onSuccess(result);
      }
      
      return result;
    } catch (err) {
      const error = err as Error;
      setError(error);
      
      if (onError) {
        onError(error);
      }
      
      throw error;
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (immediate) {
      execute();
    }
  }, []);

  return {
    data,
    loading,
    error,
    execute,
    refetch: execute,
  };
}
```

---

## 🎨 PASO 7: Ejemplos de Uso en Componentes

### 7.1 Ejemplo: Página de Login

**Crear/Modificar**: `src/pages/Login.tsx`

```typescript
// src/pages/Login.tsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';

export function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const result = await login(email, password);
      
      if (result.success) {
        navigate('/dashboard');
      } else {
        setError(result.error || 'Login failed');
      }
    } catch (err: any) {
      setError(err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <h1>Login to OWLY CRM</h1>
      
      {error && (
        <div className="alert alert-error">{error}</div>
      )}
      
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        
        <div>
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        
        <button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
    </div>
  );
}
```

### 7.2 Ejemplo: Listar Leads

**Ejemplo de componente**: `src/pages/LeadsPage.tsx`

```typescript
// src/pages/LeadsPage.tsx
import { useState, useEffect } from 'react';
import { leadsService } from '@/services/leads.service';
import type { Lead } from '@/types/lead';

export function LeadsPage() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    status: '',
    priority: '',
    search: '',
  });

  useEffect(() => {
    fetchLeads();
  }, [filters]);

  const fetchLeads = async () => {
    try {
      setLoading(true);
      const response = await leadsService.getLeads(filters);
      setLeads(response.results || []);
    } catch (error) {
      console.error('Error fetching leads:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusChange = async (leadId: string, newStatus: string) => {
    try {
      await leadsService.changeStatus(leadId, newStatus);
      fetchLeads(); // Refresh list
    } catch (error) {
      console.error('Error changing status:', error);
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="leads-page">
      <h1>Leads</h1>
      
      {/* Filters */}
      <div className="filters">
        <input
          type="text"
          placeholder="Search..."
          value={filters.search}
          onChange={(e) => setFilters({ ...filters, search: e.target.value })}
        />
        
        <select
          value={filters.status}
          onChange={(e) => setFilters({ ...filters, status: e.target.value })}
        >
          <option value="">All Status</option>
          <option value="new">New</option>
          <option value="contacted">Contacted</option>
          <option value="qualified">Qualified</option>
        </select>
      </div>

      {/* Leads Table */}
      <table>
        <thead>
          <tr>
            <th>Lead #</th>
            <th>Name</th>
            <th>Email</th>
            <th>Status</th>
            <th>Score</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {leads.map((lead) => (
            <tr key={lead.id}>
              <td>{lead.leadNumber}</td>
              <td>{lead.firstName} {lead.lastName}</td>
              <td>{lead.email}</td>
              <td>{lead.status}</td>
              <td>{lead.leadScore}</td>
              <td>
                <button onClick={() => handleStatusChange(lead.id, 'contacted')}>
                  Mark Contacted
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

### 7.3 Ejemplo: Dashboard con Analytics

```typescript
// src/pages/Dashboard.tsx
import { useApi } from '@/hooks/useApi';
import { apiClient } from '@/services/api.client';
import { API_ENDPOINTS } from '@/config/api';

export function DashboardPage() {
  const { data: stats, loading } = useApi(() =>
    apiClient.get(API_ENDPOINTS.analytics.dashboard)
  );

  if (loading) {
    return <div>Loading dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      
      <div className="metrics-grid">
        <div className="metric-card">
          <h3>Total Leads</h3>
          <p className="metric-value">{stats?.leads?.total || 0}</p>
        </div>
        
        <div className="metric-card">
          <h3>Qualified Leads</h3>
          <p className="metric-value">{stats?.leads?.qualified || 0}</p>
        </div>
        
        <div className="metric-card">
          <h3>Active Projects</h3>
          <p className="metric-value">{stats?.projects?.active || 0}</p>
        </div>
        
        <div className="metric-card">
          <h3>Quotes Sent</h3>
          <p className="metric-value">{stats?.quotes?.sent || 0}</p>
        </div>
      </div>
    </div>
  );
}
```

---

## 🔧 PASO 8: Mapear Tipos TypeScript a Modelos Django

### 8.1 Actualizar tipos existentes

Los tipos en `src/types/` necesitan ajustes menores para match con la API:

**Cambios necesarios en `src/types/lead.ts`**:

```typescript
// src/types/lead.ts

// ANTES (frontend actual):
export interface Lead {
  id: string;
  leadNumber: string;  // camelCase
  firstName: string;
  // ...
}

// DESPUÉS (para match con API):
export interface Lead {
  id: string;
  lead_number: string;  // snake_case (como viene de la API)
  first_name: string;
  last_name: string;
  // ...
  
  // O crea un transformer:
  // API usa snake_case, frontend usa camelCase
}
```

### 8.2 Crear transformers (Opción Recomendada)

**Crear**: `src/utils/transformers.ts`

```typescript
// src/utils/transformers.ts

/**
 * Transform API lead (snake_case) to frontend format (camelCase)
 */
export function transformLeadFromApi(apiLead: any): Lead {
  return {
    id: apiLead.id,
    leadNumber: apiLead.lead_number,
    firstName: apiLead.first_name,
    lastName: apiLead.last_name,
    email: apiLead.email,
    phone: apiLead.phone,
    status: apiLead.status,
    priority: apiLead.priority,
    source: apiLead.source,
    leadScore: apiLead.lead_score,
    aiCloseProbability: apiLead.ai_close_probability,
    assignedTo: apiLead.assigned_to,
    // ... mapear todos los campos
  };
}

/**
 * Transform frontend lead to API format
 */
export function transformLeadToApi(lead: Partial<Lead>): any {
  return {
    first_name: lead.firstName,
    last_name: lead.lastName,
    email: lead.email,
    phone: lead.phone,
    status: lead.status,
    priority: lead.priority,
    // ... mapear todos los campos
  };
}
```

---

## 🔧 PASO 9: Proteger Rutas

### 9.1 Protected Route Component

**Crear**: `src/components/ProtectedRoute.tsx`

```typescript
// src/components/ProtectedRoute.tsx
import { Navigate } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requireAdmin?: boolean;
  requireManager?: boolean;
}

export function ProtectedRoute({ 
  children, 
  requireAdmin = false,
  requireManager = false 
}: ProtectedRouteProps) {
  const { user, loading, isAuthenticated, isAdmin, isManager } = useAuth();

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (requireAdmin && !isAdmin) {
    return <Navigate to="/unauthorized" replace />;
  }

  if (requireManager && !isManager) {
    return <Navigate to="/unauthorized" replace />;
  }

  return <>{children}</>;
}
```

### 9.2 Uso en Routes

```typescript
// src/routes/AppRoutes.tsx
import { Routes, Route } from 'react-router-dom';
import { ProtectedRoute } from '@/components/ProtectedRoute';
import { LoginPage } from '@/pages/Login';
import { DashboardPage } from '@/pages/Dashboard';
import { LeadsPage } from '@/pages/LeadsPage';
import { AdminPage } from '@/pages/AdminPage';

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/leads"
        element={
          <ProtectedRoute>
            <LeadsPage />
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/admin"
        element={
          <ProtectedRoute requireAdmin>
            <AdminPage />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}
```

---

## 📊 PASO 10: Integrar con Estado Global (Zustand/Redux)

### 10.1 Store de autenticación con Zustand

**Crear**: `src/stores/authStore.ts`

```typescript
// src/stores/authStore.ts
import { create } from 'zustand';
import { authService } from '@/services/auth.service';

interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
  company_name: string;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,

  login: async (email, password) => {
    await authService.login({ email, password });
    const user = await authService.getCurrentUser();
    set({ user, isAuthenticated: true });
  },

  logout: () => {
    authService.logout();
    set({ user: null, isAuthenticated: false });
  },

  refreshUser: async () => {
    try {
      const user = await authService.getCurrentUser();
      set({ user, isAuthenticated: true });
    } catch (error) {
      set({ user: null, isAuthenticated: false });
    }
  },
}));
```

### 10.2 Store de Leads

```typescript
// src/stores/leadsStore.ts
import { create } from 'zustand';
import { leadsService } from '@/services/leads.service';
import type { Lead } from '@/types/lead';

interface LeadsState {
  leads: Lead[];
  loading: boolean;
  filters: any;
  setFilters: (filters: any) => void;
  fetchLeads: () => Promise<void>;
  createLead: (data: any) => Promise<void>;
  updateLead: (id: string, data: any) => Promise<void>;
}

export const useLeadsStore = create<LeadsState>((set, get) => ({
  leads: [],
  loading: false,
  filters: {},

  setFilters: (filters) => set({ filters }),

  fetchLeads: async () => {
    set({ loading: true });
    try {
      const response = await leadsService.getLeads(get().filters);
      set({ leads: response.results || [] });
    } catch (error) {
      console.error('Error fetching leads:', error);
    } finally {
      set({ loading: false });
    }
  },

  createLead: async (data) => {
    await leadsService.createLead(data);
    await get().fetchLeads();
  },

  updateLead: async (id, data) => {
    await leadsService.updateLead(id, data);
    await get().fetchLeads();
  },
}));
```

---

## 🚦 PASO 11: Testing de Integración Frontend

### 11.1 Mock de la API

**Crear**: `src/mocks/apiMocks.ts`

```typescript
// src/mocks/apiMocks.ts
import { rest } from 'msw';
import { API_BASE_URL } from '@/config/api';

export const handlers = [
  // Login
  rest.post(`${API_BASE_URL}/auth/login/`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        access: 'mock-access-token',
        refresh: 'mock-refresh-token',
      })
    );
  }),

  // Get Profile
  rest.get(`${API_BASE_URL}/auth/users/profile/`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        id: '123',
        email: 'test@test.com',
        full_name: 'Test User',
        role: 'sales',
      })
    );
  }),

  // Get Leads
  rest.get(`${API_BASE_URL}/leads/`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        count: 2,
        results: [
          {
            id: '1',
            lead_number: 'LEAD-2024-001',
            first_name: 'John',
            last_name: 'Doe',
            email: 'john@test.com',
            status: 'new',
          },
        ],
      })
    );
  }),
];
```

---

## 📋 PASO 12: Checklist de Integración

### Pre-requisitos:
- [ ] API corriendo en http://localhost:8000
- [ ] Frontend corriendo en http://localhost:5173
- [ ] CORS configurado en API
- [ ] Superuser creado en API

### Archivos a Crear en Frontend:
- [ ] `src/config/api.ts` - Configuración de endpoints
- [ ] `src/services/auth.service.ts` - Servicio de autenticación
- [ ] `src/services/api.client.ts` - Cliente API genérico
- [ ] `src/services/leads.service.ts` - Servicio de leads
- [ ] `src/services/projects.service.ts` - Servicio de projects
- [ ] `src/hooks/useAuth.ts` - Hook de autenticación
- [ ] `src/hooks/useApi.ts` - Hook genérico de API
- [ ] `src/utils/transformers.ts` - Transformadores de datos
- [ ] `src/components/ProtectedRoute.tsx` - Rutas protegidas

### Integración:
- [ ] Login funciona y guarda tokens
- [ ] Requests incluyen Authorization header
- [ ] Token refresh automático funciona
- [ ] Rutas protegidas verifican autenticación
- [ ] Logout limpia tokens
- [ ] Errores se manejan correctamente

---

## 🎯 Flujo Completo de Autenticación

```
1. Usuario abre app
   ↓
2. Frontend verifica si hay token en localStorage
   ↓
3a. SI hay token:
    → Llama GET /api/auth/users/profile/
    → Obtiene datos del usuario
    → Muestra dashboard
    
3b. NO hay token:
    → Redirige a /login

4. Usuario hace login:
   POST /api/auth/login/
   {email, password}
   ↓
   Recibe {access, refresh}
   ↓
   Guarda en localStorage
   ↓
   Redirige a /dashboard

5. Usuario hace request:
   GET /api/leads/
   Header: Authorization: Bearer {access_token}
   ↓
   API valida token
   ↓
   Devuelve leads de la empresa del usuario

6. Access token expira (después de 1 hora):
   Request falla con 401
   ↓
   AuthService automáticamente llama:
   POST /api/auth/refresh/
   {refresh: refresh_token}
   ↓
   Recibe nuevo access token
   ↓
   Retry el request original
   ↓
   Usuario no nota nada

7. Refresh token expira (después de 7 días):
   → Logout automático
   → Redirige a /login
```

---

## 🔄 Mapeo de Endpoints a Componentes

| Frontend Component | API Endpoints | Descripción |
|-------------------|---------------|-------------|
| `LoginPage` | `POST /api/auth/login/` | Login con JWT |
| `DashboardPage` | `GET /api/analytics/dashboard/` | Stats generales |
| `LeadsPage` | `GET /api/leads/` | Listar leads |
| `LeadDetailPage` | `GET /api/leads/{id}/`<br/>`GET /api/leads/{id}/timeline/` | Detalle y timeline |
| `ProjectsPage` | `GET /api/projects/` | Listar proyectos |
| `ProjectDetailPage` | `GET /api/projects/{id}/`<br/>`GET /api/projects/{id}/units/` | Proyecto y unidades |
| `QuotesPage` | `GET /api/quotes/` | Listar cotizaciones |
| `RadarPage` | `GET /api/leads/hot_leads/` | Leads calientes |
| `CalendarPage` | `GET /api/leads/upcoming_followups/` | Follow-ups |

---

## ⚡ Quick Start de Integración

### Opción 1: Solo Autenticación Primero

```typescript
// 1. Crear auth.service.ts (código de arriba)
// 2. Crear useAuth.ts (código de arriba)
// 3. Modificar LoginPage para usar authService
// 4. Probar login → ¡Ya tienes auth funcionando!
```

### Opción 2: Integración Completa

```typescript
// 1. Crear todos los archivos de servicios
// 2. Crear hooks (useAuth, useApi)
// 3. Crear stores (Zustand/Redux)
// 4. Actualizar componentes página por página
// 5. Testing de cada integración
```

---

## 🐛 Troubleshooting

### Error: CORS

```
Access to fetch at 'http://localhost:8000/api/leads/' from origin 
'http://localhost:5173' has been blocked by CORS policy
```

**Solución**:
1. Verificar `CORS_ALLOWED_ORIGINS` en `owly-api-django/.env`
2. Incluir puerto exacto: `http://localhost:5173`
3. Reiniciar: `docker-compose restart web`

### Error: 401 Unauthorized

```
{"detail": "Authentication credentials were not provided."}
```

**Solución**:
1. Verificar que incluyes header: `Authorization: Bearer {token}`
2. Verificar que token no expiró
3. Verificar formato: "Bearer" (con mayúscula y espacio)

### Error: Token expired

**Solución**: Ya manejado en `authService.makeAuthenticatedRequest()`
- Detecta 401
- Llama automáticamente a refresh
- Retry request
- Si falla, logout

---

## 📚 Documentación de Referencia

Para cada endpoint, consulta:
- **Intención**: `ENDPOINTS_GUIDE.md`
- **Request/Response**: http://localhost:8000/api/docs/
- **Modelos**: `MODELS_DOCUMENTATION.md`

---

## ✅ Checklist Final

- [ ] CORS configurado en API
- [ ] `.env` creado en frontend con API_URL
- [ ] `api.ts` creado con endpoints
- [ ] `auth.service.ts` creado
- [ ] `api.client.ts` creado
- [ ] Services creados (leads, projects, etc.)
- [ ] Hooks creados (useAuth, useApi)
- [ ] Login page actualizada
- [ ] Protected routes implementadas
- [ ] Dashboard consume API analytics
- [ ] Primera integración funcionando

---

**Siguiente**: Lee la guía de mejoras de Projects/Units en el próximo documento.

