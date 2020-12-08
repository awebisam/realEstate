from blog.models import Blog
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.auth.models import User


def check(x):
    if x == "on" or x == "yes":
        return True
    else:
        return False


def index(request):
    latest = Property.objects.filter(published=True, paid=True)[:6]
    blogs = Blog.blogs.all()[:3]
    context = {
        'latest': latest,
        'blogs': blogs,
    }
    return render(request, 'core/index.html', context)


def properties(request):
    if request.method == 'POST':
        ptype = request.POST.get('type')
        status = request.POST.get('status')
        address = request.POST.get('address')
        maxprice = request.POST.get('maxprice')
        queryset_list = Property.objects.filter(
            published=True)
        if ptype != "Any Type":
            queryset_list = queryset_list.filter(ptype=ptype)
        if status != "Any Status":
            queryset_list = queryset_list.filter(status=status)
        if address:
            queryset_list = queryset_list.filter(address__icontains=address)
        if maxprice:
            queryset_list = queryset_list.filter(price__lte=maxprice)

        paginator = Paginator(queryset_list, 6)
        page = request.GET.get('page')
        paged_listings = paginator.get_page(page)

        context = {
            'listings': paged_listings,
            'ptype': ptype,
            'status': status,
            'address': address,
            'maxprice': maxprice,
        }

        return render(request, 'core/list.html', context)
    else:
        queryset_list = Property.objects.filter(published=True)

    paginator = Paginator(queryset_list, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings
    }

    return render(request, 'core/list.html', context)


@login_required(login_url="/authentication/login/")
def post_prop(request):
    """
    View to handle post property
    """
    if request.method == "POST" or request.method == "FILES":
        userr = request.POST.get('added_by')
        added_by = User.objects.get(id=userr)
        title = request.POST.get('title')
        status = request.POST.get('status')
        ptype = request.POST.get('ptype')
        area = request.POST.get('area')
        number_of_rooms = request.POST.get('number_of_rooms')
        price = request.POST.get('price')
        has_installment = check(request.POST.get('has_installment'))
        has_insurance = check(request.POST.get('has_insurance'))
        description = request.POST.get('description')
        address = request.POST.get('address')
        garden = check(request.POST.get('garden'))
        garage = check(request.POST.get('garage'))
        swimming_pool = check(request.POST.get('swimming_pool'))
        bathtub = check(request.POST.get('bathtub'))
        ac = check(request.POST.get('ac'))
        internet = check(request.POST.get('internet'))
        play_ground = check(request.POST.get('play_ground'))
        photo = request.FILES.get('photo')
        video = request.POST.get('video')
        phone = request.POST.get('phone')
        paid = check(request.POST.get('paid'))

        properti = Property(added_by=added_by, title=title, status=status, ptype=ptype, area=area, number_of_rooms=number_of_rooms, price=price, has_installment=has_installment, has_insurance=has_insurance, description=description,
                            address=address, phone=phone, garden=garden, garage=garage, video=video, swimming_pool=swimming_pool, bathtub=bathtub, ac=ac, internet=internet, play_ground=play_ground, photo=photo, paid=paid)
        properti.save()
        email = EmailMessage(
            f'New {ptype} on Sajilo Realestate ',
            f'''
            There was a post of {title} by {added_by}.
            Email: {added_by.email}
            Phone: {phone}
            Wants to get it featured?? {paid}
            ''',
            'no_reply@sajilorealestate.com',
            to=['hi@sajilorealestate.com', ],
            reply_to=[f'{added_by.email}', ],
        )
        email.send(fail_silently=False)
        messages.success(
            request, 'Successfully Posted. Please wait till it gets verified.')
        return redirect('core_app:post')
    return render(request, 'core/post.html')


def property_detail(request, slug):
    property_detail = Property.objects.get(slug=slug)
    return render(request, 'core/property.html', {'p': property_detail})


@login_required(login_url="/authentication/login/")
def inquiry(request):
    if request.method == 'GET':
        return redirect('core_app:list')
    elif request.method == 'POST':
        inq = request.POST
        prop = inq.get('property')
        message = inq.get('message')
        name = inq.get('name')
        email = inq.get('email')
        phone = inq.get('phone')
        u = inq.get('user')
        path = inq.get('path')
        properti = Property.objects.get(id=prop)
        print('got')
        if u is not None:
            user = User.objects.get(username=u)
            inquiry = Inquiry(prop=properti, message=message, name=name,
                              email=email, phone=phone, user=user)
        else:
            inquiry = Inquiry(prop=properti, message=message, name=name,
                              email=email, phone=phone)
        inquiry.save()
        print('saved')
        email = EmailMessage(
            f'New inquiry in {properti} ',
            f'''
            There was a new inquiry on {properti} by {name}.
            Email: {email}
            Phone: {phone}
            Message: {message}
            ''',
            'no_reply@sajilorealestate.com',
            to=['awebisam@gmail.com', ],
            reply_to=[f'{email}', ],
        )
        try:
            email.send(fail_silently=False)
            messages.success(
                request, 'Inquiry successful. Please wait for any response.')
            return HttpResponseRedirect(path)

        except:
            messages.danger(
                request, 'There was an error. Please recheck your form data or contact us via phone.')
            return HttpResponseRedirect(path)


@login_required(login_url="/authentication/login/")
def queries(request):
    if not request.user.is_authenticated:
        return redirect('core_app:index')
    else:
        queries = Inquiry.objects.filter(user=request.user, done=False)
        print(queries)
        return render(request, 'core/queries.html', {'queries': queries})


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    if request.method == "POST":
        ct = request.POST
        firstname = ct.get('firstname')
        lastname = ct.get('lastname')
        email = ct.get('email')
        phone = ct.get('phone')
        message = ct.get('message')
        mes = Message(first_name=firstname, last_name=lastname,
                      phone=phone, email=email, message=message)
        mes.save()
        email = EmailMessage(
            f'New message by {firstname} ',
            f'''
            Name: {firstname} {lastname}
            Email: {email}
            Phone: {phone}
            Message: {message}
            ''',
            'no_reply@sajilorealestate.com',
            to=['hi@sajilorealestate.com', ],
            reply_to=[f'{email}', ],
        )
        try:
            email.send(fail_silently=False)
            messages.success(
                request, 'Your message has been sent. Please wait for our response.')
            return redirect('core_app:contact')

        except:
            messages.error(
                request, 'There was an error. Please recheck your data or contact us via phone.')
            return redirect('core_app:contact')

    return render(request, 'core/contact.html')
