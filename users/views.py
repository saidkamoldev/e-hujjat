from django.shortcuts import render, redirect
from django.views.generic import View
from admins.models import User, Organization, Table
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.db.models import Case, When, Value, BooleanField

class UserDashboard(View):
    def get(self, request):
        context = {}
        user = request.user
        end_date = timezone.now()
        tables = Table.objects.select_related('user', 'organization').all().order_by('-id')[:7]
        all_count = Table.objects.filter(user_id = user.id).count()
        inactive_count = Table.objects.filter(status=False, user_id = user.id).count()
        active_count = Table.objects.filter(status=True, user_id = user.id).count()
        thirty_days_ago = end_date - timedelta(minutes=2)
        inactive_old_count = Table.objects.filter(
            status=False,
            user_id = user.id,
            created_at__lt=thirty_days_ago
        ).count()

        #PIZZA
        organizations = Organization.objects.all()
        array_organizations = []
        array_count_organizations = []
        for organization in organizations:
            array_organizations.append(organization.title)
            count = Table.objects.filter(organization=organization, user_id = user.id).count()
            array_count_organizations.append(count)
        #PIZZA


        #LINE CHART
        start_date = end_date - timedelta(days=7)
        weekly_data = (
            Table.objects.filter(status=True, user_id = user.id, created_at__range=[start_date, end_date])
            .extra(select={'day': 'date(created_at)'})
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )
        labels = [entry['day'] for entry in weekly_data]
        data = [entry['count'] for entry in weekly_data]
        #LINE CHART

        context.update({
            'tables': tables,
            'all_count': all_count,
            'inactive_count': inactive_count,
            'active_count': active_count,
            'inactive_old_count': inactive_old_count,
            'array_organizations': array_organizations,
            'array_count_organizations': array_count_organizations,
            'labels': labels,
            'data': data
        })

        return render(request, 'user/dashboard.html', context)

class UserRequest(View):
    def get(self, request):
        user = request.user
        if user.role != 'user':
            return redirect('login')
        tables = Table.objects.select_related('user', 'organization') \
            .order_by('-id') \
            .annotate(
                no_id=Case(
                    When(user__id=user.id, then=Value(False)),
                    default=Value(True),
                    output_field=BooleanField()
                )
            )

        context = {
            'tables': tables
        }

        return render(request, 'user/tables.html', context)


class UserRequestCreate(View):
    def get(self, request):
        user = request.user
        if user.role != 'user':
            return redirect('login')
        context = {}
        organizations = Organization.objects.all().values('id', 'title')
        context.update({
            'organizations': organizations
        })
        return render(request, 'user/create_table.html', context)
    
    def post(self, request):
        user = request.user
        if user.role != 'user':
            return redirect('login')
        organization_id = request.POST.get('organization')
        
        user = User.objects.get(id=user.id)
        organization = Organization.objects.get(id=organization_id)
        
        Table.objects.create(user=user, organization=organization)
        return redirect('user_requests')

class UserChangeStatus(View):
    def post(self, request):
        user = request.user
        if user.role != 'user':
            return redirect('login')
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
        return redirect('user_requests')

class UserRequestUpdate(View):
    def get(self, request):
        user = request.user
        if user.role != 'user':
            return redirect('login')
        context = {}
        table_id = request.GET.get('id')
        table = Table.objects.select_related('user', 'organization').get(id=table_id)
        organizations = Organization.objects.all().values('id', 'title')
        context.update({
            'table': table,
            'organizations': organizations
        })
        return render(request, 'user/update_table.html', context)
    def post(self, request):
        user = request.user
        if user.role != 'user':
            return redirect('login')
        table_id = request.GET.get('id')
        table = Table.objects.select_related('user', 'organization').get(id=table_id)
        organization_id = request.POST.get('organization')
        user = User.objects.get(id=user.id)
        organization = Organization.objects.get(id=organization_id)
        status = request.POST.get('status') == 'True'
        if(table.user != user or table.organization != organization or table.status != status):
            table.user = user
            table.organization = organization
            table.status = status
            table.save()
            return redirect('user_requests')
        return redirect('user_requests')

class UserOrganizations(View):
    def get(self, request):
        user = request.user
        if user.role != 'user':
            return redirect('login')
        context = {}
        organizations = Organization.objects.all().order_by('-id')
        context.update({
            'organizations': organizations
        })
        return render(request, 'user/organizations.html', context)

class UserOrganizationsCreate(View):
    def get(self, request):
        user = request.user
        if user.role != 'user':
            return redirect('login')
        return render(request, 'user/create_organizations.html')
    
    def post(self, request):
        user = request.user
        if user.role != 'user':
            return redirect('login')
        title = request.POST.get('title')
        org_exists = Organization.objects.filter(title=title).exists()
        if not org_exists:
            Organization.objects.create(title=title)
        return redirect('user_organizations')
