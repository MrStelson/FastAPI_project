import aiohttp
from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi_users.exceptions import UserAlreadyExists
import starlette.status as status

from src.ad.router import get_type, get_ad, get_ad_by_type, get_category, get_type_id, get_ad_by_id_user, delete_ad, \
    get_ad_by_id, get_ad_comments

from src.ad.service import get_category_by_name
from src.auth.config import current_user
from src.auth.manager import get_user_manager, UserManager
from src.auth.models import User
from src.auth.schemas import UserCreate
from src.auth.service import get_all_users, banned_users, add_admin
from src.config import API_URL, HOST_PORT

router = APIRouter(
    prefix="",
    tags=["App"]
)

templates = Jinja2Templates(directory="src/templates")

HOME_URL = f'http://localhost:{HOST_PORT}'


async def http_response_post(url, json_data=None, data_data=None, cookies=None):
    async with aiohttp.ClientSession(trust_env=True) as session:
        response = await session.post(url=url,
                                      json=json_data,
                                      data=data_data,
                                      cookies=cookies,
                                      )
        return response


@router.get("/")
async def get_base_page(request: Request, types=Depends(get_type),
                        user=Depends(current_user),
                        ads=Depends(get_ad),
                        ):
    data = {"request": request, "types": types["data"], "user": user, "ads": ads["data"]}
    return templates.TemplateResponse("index.html", data)


@router.get('/ad/{ad_id}')
async def get_ad_by_id(request: Request,
                       types=Depends(get_type),
                       user=Depends(current_user),
                       ad=Depends(get_ad_by_id),
                       comments=Depends(get_ad_comments)):
    return templates.TemplateResponse("ad_page.html", {"request": request,
                                                       "types": types["data"],
                                                       "user": user,
                                                       "ad": ad["data"][0],
                                                       "category": ad["data"][1],
                                                       "type": ad["data"][2],
                                                       "comments": comments["data"],
                                                       })


@router.get("/login")
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login_post(request: Request,
                     email: str = Form(...),
                     password: str = Form(...)):
    data = {"username": email, "password": password}
    url = f'{HOME_URL}/{API_URL}/auth/jwt/login'
    response = await http_response_post(url=url, data_data=data)
    redirect = RedirectResponse(url=f'{request.base_url}', status_code=status.HTTP_302_FOUND)
    redirect.set_cookie(key='advertisement_auth', value=response.cookies.get('advertisement_auth'))
    return redirect


@router.get("/logout")
async def logout(request: Request):
    response = RedirectResponse('/', status_code=302)
    response.delete_cookie(key='advertisement_auth')
    return response


@router.get("/registry")
async def registry_get(request: Request):
    return templates.TemplateResponse("registry.html", {"request": request})


@router.post("/registry")
async def registry_post(request: Request,
                        user_manager: UserManager = Depends(get_user_manager),
                        email: str = Form(...),
                        username: str = Form(...),
                        password: str = Form(...),
                        ):
    data = {"email": email,
            "password": password,
            "username": username,
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "role_id": 0,
            "is_banned": False}
    errors = []
    try:
        await user_manager.create(user_create=UserCreate(**data))
    except UserAlreadyExists:
        errors.append(f'User with {email} already exists')
        return templates.TemplateResponse("registry.html", {"request": request, "errors": errors})
    redirect = RedirectResponse(url='/login')
    return redirect


@router.get("/type/{type_id}")
async def get_base_page_type(request: Request,
                             types=Depends(get_type),
                             user=Depends(current_user),
                             type_name=Depends(get_type_id),
                             ads=Depends(get_ad_by_type)):
    return templates.TemplateResponse("index.html", {"request": request,
                                                     "types": types["data"],
                                                     "user": user,
                                                     "ads": ads["data"],
                                                     "type_name": type_name["data"][0]["type_name"]
                                                     })


@router.get("/add")
async def add_ad_get(request: Request,
                     types=Depends(get_type),
                     cats=Depends(get_category),
                     user=Depends(current_user)):
    return templates.TemplateResponse("add_ad.html", {"request": request,
                                                      "types": types["data"],
                                                      "cats": cats["data"],
                                                      "user": user,
                                                      })


@router.post("/add")
async def add_ad_post(request: Request,
                      title: str = Form(...),
                      category_name: str = Form(...),
                      price: str = Form(...),
                      description: str = Form(...),
                      user=Depends(current_user),
                      ):
    redirect = RedirectResponse(url=f'{request.base_url}', status_code=status.HTTP_302_FOUND)

    if user is None:
        return redirect
    if user.is_banned:
        return redirect

    category_id = await get_category_by_name(category_name)
    data = {"name": title,
            "category_id": category_id,
            "description": description,
            "price": price,
            "user_id": user.id,
            }
    url = f'{HOME_URL}/{API_URL}/ad/'
    cookie = {'advertisement_auth': request.cookies.get('advertisement_auth')}
    await http_response_post(url=url, json_data=data, cookies=cookie)
    return redirect


@router.get('/editUsers')
async def edit_users_get(request: Request,
                         user: User = Depends(current_user),
                         users_list=Depends(get_all_users)):
    if user is None:
        return {
            "status": 401,
            "data": None,
            "detail": "Don't have access. Please authorisation"
        }

    if user.role_id == 3:
        return templates.TemplateResponse("users.html", {"request": request,
                                                         "user": user,
                                                         "users": users_list})
    else:
        return {
            "status": 401,
            "data": None,
            "detail": "Don't have access"
        }


@router.get('/user/{user_id}')
async def user_page(request: Request, types=Depends(get_type),
                    user=Depends(current_user), ads=Depends(get_ad_by_id_user)):
    return templates.TemplateResponse("user_page.html", {"request": request,
                                                         "types": types["data"],
                                                         "user": user,
                                                         "ads": ads["data"],
                                                         })


@router.get('/editUsers/banned/{user_id}')
async def edit_users_get(request: Request,
                         user_id: int,
                         user: User = Depends(current_user)):
    if user is None:
        return {
            "status": 401,
            "data": None,
            "detail": "Don't have access. Please authorisation"
        }

    if user.role_id == 3:
        await banned_users(user_id=user_id)
        redirect = RedirectResponse(url=f'/editUsers', status_code=status.HTTP_302_FOUND)
        return redirect
    else:
        return {
            "status": 401,
            "data": None,
            "detail": "Don't have access"
        }


@router.get('/editUsers/admin/{user_id}')
async def edit_users_get(request: Request,
                         user_id: int,
                         user: User = Depends(current_user)):
    if user is None:
        return {
            "status": 401,
            "data": None,
            "detail": "Don't have access. Please authorisation"
        }

    if user.role_id == 3:
        await add_admin(user_id=user_id)
        redirect = RedirectResponse(url=f'/editUsers', status_code=status.HTTP_302_FOUND)
        return redirect
    else:
        return {
            "status": 401,
            "data": None,
            "detail": "Don't have access"
        }


@router.get('/ad/delete/{ad_id}')
async def delete_ad(request: Request,
                    deleted_ad=Depends(delete_ad)):
    redirect = RedirectResponse(url=f'/', status_code=status.HTTP_302_FOUND)
    return redirect
