import random
import uuid
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from core.models.auth import OTP, User
from django.contrib.auth.decorators import login_required

from base.helper import code_decoder, generate_key


def sign_up(request):
    ctx = {}
    if request.POST:
        data = request.POST
        fio = data.get('fio', None)
        password = data.get('password', None)
        phone = data.get('phone', None)
        if None in [fio, password, phone]:
            ctx['error'] = 'Malumotlarni toliq kiriting'
            return render(request, 'auth/register.html', ctx)
        phone = phone.replace('+', '')
        find_user = User.objects.filter(phone=phone).filter()
        if find_user:
            ctx['error'] = 'Bunday user bor'
            return render(request, 'auth/register.html', ctx)

        # send password
        number = random.randint(100_000, 999_999)
        hash = f'{generate_key(15)}${number}${uuid.uuid4().__str__()}'
        hashed = code_decoder(hash, decode=False, l=settings.HASHED_LENGTH)
        otp = OTP.objects.create(
            key=hashed,
            mobile=phone,
            extra={'fio': fio, 'password': code_decoder(password)},
            step='regis'
        )
        request.session['key'] = otp.key
        request.session['otp'] = number

        return redirect('step_two')
    return render(request, 'auth/register.html', ctx)


def step_two(request):
    ctx = {}
    key = request.session.get('key', None)
    if not key:
        return redirect('sign_in')

    if request.POST:
        otp = ''
        for i in range(1, 7):
            otp += request.POST.get(f'otp{i}', '')
        otp_base = OTP.objects.filter(key=key).first()
        if not otp_base:
            ctx['error'] = 'Kalit topilmadi. Boshqattan royhatdan oting'
            return render(request, 'auth/step_two.html', ctx)

        if otp_base.is_verified or otp_base.is_expired:
            ctx['error'] = 'Bu token allaqachon eskirgan'
            return render(request, 'auth/step_two.html', ctx)

        if not otp_base.check_expire_date():
            ctx['error'] = 'Bu tokenga ajratilgan vaht tugadi'
            return render(request, 'auth/step_two.html', ctx)

        decode = code_decoder(key, decode=True, l=settings.HASHED_LENGTH)
        code = decode.split('$')[1]
        if str(otp) != str(code):
            otp_base.tries += 1
            otp_base.save()
            ctx['error'] = 'Kod Xato'
            return render(request, 'auth/step_two.html', ctx)

        if otp_base.step == 'regis':
            extra = otp_base.extra
            pas = extra.pop("password")
            user = User.objects.create_user(
                phone=otp_base.mobile,
                password=code_decoder(pas, decode=True),
                **extra,
            )
            login(request, user)
            authenticate(request)

            return redirect('home')

        if otp_base.step == 'login':
            user = User.objects.filter(phone=otp_base.mobile).first()

            if user:
                login(request, user)
                return redirect('home')
            else:
                ctx['error'] = 'Foydalanuvchi topilmadi'
                return render(request, 'auth/step_two.html', ctx)

    return render(request, 'auth/step_two.html', ctx)


def sign_in(request):
    ctx = {}
    if request.POST:
        data = request.POST
        password = data.get('password', None)
        phone = data.get('phone', None)
        if None in [password, phone]:
            ctx['error'] = 'Malumotlarni toliq kiriting'
            return render(request, 'auth/login. html', ctx)
        user = User.objects.filter(phone=phone).first()
        if user is None:
            ctx['error'] = 'Foydalanuvchi topilmadi'
            return render(request, 'auth/login.html', ctx)

        if not user.check_password(password):
            ctx['error'] = 'Parol notogri'
            return render(request, 'auth/login.html', ctx)

        number = random.randint(100_000, 999_999)
        hash = f'{generate_key(15)}${number}${uuid.uuid4().__str__()}'
        hashed = code_decoder(hash, decode=False, l=settings.HASHED_LENGTH)
        otp = OTP.objects.create(
            key=hashed,
            mobile=phone,
            step='login'
        )
        request.session['key'] = otp.key
        request.session['otp'] = number

        return redirect('step_two')
    return render(request, 'auth/login.html', ctx)


@login_required(login_url='login')
def sign_out(request):
    logout(request)
    return redirect('login')






