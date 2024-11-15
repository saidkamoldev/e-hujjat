from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.http.response import Http404
from django.views.generic import View
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from admins.models import User, Organization, Table
from django.db.models import Count
from django.contrib.auth.hashers import make_password

def home(request):
    user = request.user
    if not request.user.is_authenticated:
        return redirect('login')
    if user.role == 'admin':
        return redirect('custom_admin')
    if user.role == 'user':
        return redirect('custom_user')
    raise Http404()

class AdminSignOut(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class UserLogin(View):
    
    def get(self, request):
        return render(request, 'login/login.html')
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if not user:
            messages.error(request, 'Invalid Phone number or password')
            return redirect('login')
        login(request, user)
        return redirect('home')

class AdminDashboard(View):

    def get(self, request):
        user = request.user
        if user.role != 'admin':
            return redirect('custom_user')
        context = {}
        end_date = timezone.now()
        # tables = Table.objects.select_related('user', 'organization').all().order_by('-id')[:7]
        all_count = Table.objects.count()
        inactive_count = Table.objects.filter(status=False).count()
        active_count = Table.objects.filter(status=True).count()
        thirty_days_ago = end_date - timedelta(minutes=1)
        inactive_old_count = Table.objects.filter(
            status=False,
            created_at__lt=thirty_days_ago
        ).count()

        #PIZZA
        organizations = Organization.objects.all()
        array_organizations = []
        array_count_organizations = []
        for organization in organizations:
            array_organizations.append(organization.title)
            count = Table.objects.filter(organization=organization).count()
            array_count_organizations.append(count)
        #PIZZA


        #LINE CHART
        start_date = end_date - timedelta(days=7)
        weekly_data = (
            Table.objects.filter(status=True, created_at__range=[start_date, end_date])
            .extra(select={'day': 'date(created_at)'})
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )
        labels = [entry['day'] for entry in weekly_data]
        data = [entry['count'] for entry in weekly_data]
        #LINE CHART

        context.update({
            # 'tables': tables,
            'all_count': all_count,
            'inactive_count': inactive_count,
            'active_count': active_count,
            'inactive_old_count': inactive_old_count,
            'array_organizations': array_organizations,
            'array_count_organizations': array_count_organizations,
            'labels': labels,
            'data': data
        })

        return render(request, 'admin/dashboard.html', context)
class AdminTables(View):
    def get(self, request):
        user = request.user
        if user.role != 'admin':
            return redirect('custom_user')
        context = {}
        tables = Table.objects.select_related('user', 'organization').all().order_by('-id')
        context.update({
            'tables': tables
        })
        return render(request, 'admin/tables.html', context)

class AdminCreateTable(View):
    def get(self, request):
        user = request.user
        if user.role != 'admin':
            return redirect('custom_user')
        context = {}
        users = User.objects.all().values('id', 'name')
        organizations = Organization.objects.all().values('id', 'title')
        context.update({
            'users': users,
            'organizations': organizations
        })
        return render(request, 'admin/create_table.html', context)

    def post(self, request):
        user = request.user
        if user.role != 'admin':
            return redirect('custom_user')
        user_id = request.POST.get('user')
        organization_id = request.POST.get('organization')
        
        user = User.objects.get(id=user_id)
        organization = Organization.objects.get(id=organization_id)
        
        Table.objects.create(user=user, organization=organization)
        return redirect('tables')

class AdminUpdateTable(View):
    def get(self, request):
        user = request.user
        if user.role != 'admin':
            return redirect('custom_user')
        context = {}
        table_id = request.GET.get('id')
        table = Table.objects.select_related('user', 'organization').get(id=table_id)
        users = User.objects.all().values('id', 'name')
        organizations = Organization.objects.all().values('id', 'title')
        context.update({
            'table': table,
            'users': users,
            'organizations': organizations
        })
        return render(request, 'admin/update_table.html', context)
    def post(self, request):
        user = request.user
        if user.role != 'admin':
            return redirect('custom_user')
        table_id = request.GET.get('id')
        table = Table.objects.select_related('user', 'organization').get(id=table_id)
        user_id = request.POST.get('user')
        organization_id = request.POST.get('organization')
        user = User.objects.get(id=user_id)
        organization = Organization.objects.get(id=organization_id)
        status = request.POST.get('status') == 'True'
        if(table.user != user or table.organization != organization or table.status != status):
            table.user = user
            table.organization = organization
            table.status = status
            table.save()
            return redirect('tables')
        return redirect('tables')

class AdminOrganizations(View):
    def get(self, request):
        user = request.user
        if user.role != 'admin':
            return redirect('custom_user')
        context = {}
        organizations = Organization.objects.all().order_by('-id')
        context.update({
            'organizations': organizations
        })
        return render(request, 'admin/organizations.html', context)

class AdminCreateOrganization(View):
    def get(self, request):
        user = request.user
        if user.role != 'admin':
            return redirect('custom_user')
        return render(request, 'admin/create_organizations.html')

    def post(self, request):
        user = request.user
        if user.role != 'admin':
            return redirect('custom_user')
        title = request.POST.get('title')
        org_exists = Organization.objects.filter(title=title).exists()
        if not org_exists:
            Organization.objects.create(title=title)
        return redirect('organizations')

class AdminUpdateOrganization(View):
    def get(self, request):
        user = request.user
        if user.role != 'admin':
            return redirect('custom_user')
        context = {}
        organization_id = request.GET.get('id')
        organization = Organization.objects.get(id=organization_id)
        context.update({
            'organization': organization
        })
        return render(request, 'admin/update_organization.html', context)
    
    def post(self, request):
        user = request.user
        if user.role != 'admin':
            return redirect('custom_user')
        organization_id = request.POST.get('id')
        title = request.POST.get('title')
        organization = Organization.objects.get(id=organization_id)
        if organization.title != title:
            organization.title = title
            organization.save()
        return redirect('organizations')

class AdminUserTable(View):
    def get(self, request):
        user = request.user
        if user.role != 'admin':
            return redirect('custom_user')
        context = {}
        users = User.objects.filter(role='user').all().order_by('-id')
        context.update({
            'users': users
        })
        return render(request, 'admin/users_table.html', context)

class AdminCreateUser(View):
    def get(self, request):
        user = request.user
        if user.role != 'admin':
            return redirect('custom_user')
        return render(request, 'admin/create_user.html')
    
    def post(self, request):
        user = request.user
        if user.role != 'admin':
            return redirect('custom_user')
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        try:
            User.objects.create_user(name=name, email=email, password=password, role=role)
            return redirect('users')
        except Exception as e:
            return render(request, 'admin/create_user.html')

class AdminUserUpdate(View):
    def get(self, request):
        user = request.user
        if user.role != 'admin':
            return redirect('custom_user')
        context = {}
        id = request.GET.get('id')
        user = User.objects.get(id=id)
        context.update({
            'user': user
        })
        return render(request, 'admin/update_user.html', context)
    
    def post(self, request):
        user = request.user
        if user.role != 'admin':
            return redirect('custom_user')
        user_id = request.POST.get('id')
        user = User.objects.get(id=user_id)
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)
        if name != user.name or email != user.email or password:
            user.name = name
            user.email = email
            if password:
                user.password = make_password(password)
            user.save()
        return redirect('users')

class AdminSatatusChange(View):
    def post(self, request):
        user = request.user
        if user.role != 'admin':
            return redirect('custom_user')
        context = {}
        table_id = request.POST.get('id')
        status = request.POST.get('status')
        try:
            table = Table.objects.get(id=table_id)
            if status == 'Active':
                table.status = True
            else:
                table.status = False
            table.save()
        except Table.DoesNotExist:
            context['error'] = "Table not found"
        return redirect('tables')

class AdminStatistica(View):
    def get(self, request):
        user = request.user
        if user.role != 'admin':
            return redirect('custom_user')
        time = request.GET.get('time', '1')
        end_date = timezone.now()
        if time != 'all':
            time = int(time)
            start_date = end_date - timedelta(days=time)
            weekly_data = (
                Table.objects.filter(status=True, created_at__range=[start_date, end_date])
                .extra(select={'day': 'date(created_at)'})
                .values('day')
                .annotate(count=Count('id'))
                .order_by('day')
            )
        else:
            weekly_data = (
                Table.objects.filter(status=True)
                .extra(select={'day': 'date(created_at)'})
                .values('day')
                .annotate(count=Count('id'))
                .order_by('day')
            )
        labels = [entry['day'] for entry in weekly_data]
        data = [entry['count'] for entry in weekly_data]
        
        #PIZZA
        organizations = Organization.objects.all()
        array_organizations = []
        array_count_organizations = []
        for organization in organizations:
            array_organizations.append(organization.title)
            count = Table.objects.filter(organization=organization).count()
            array_count_organizations.append(count)
        #PIZZA

        context = {
            'labels': labels,
            'data': data,
            'array_organizations': array_organizations,
            'array_count_organizations': array_count_organizations,
        }
        return render(request, 'admin/statistica.html', context)


class AdminSetting(View):
    def get(self, request):
        user = request.user
        if user.role != 'admin':
            return redirect('custom_user')
        context = {}
        user = request.user
        context.update({
            'user': user
        })
        return render(request, 'admin/settings_admin.html', context)
    
    def post(self, request):
        user = request.user
        if user.role != 'admin':
            return redirect('custom_user')
        user = request.user
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if user.name != name or user.email != email or password:
            user.name = name
            user.email = email
            if password:
                user.password = make_password(password)
            user.save()
            logout(request)
            return redirect('login')
        return redirect('custom_admin')
    
