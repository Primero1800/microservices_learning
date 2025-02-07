import inspect
from typing import Callable, Any

# from fastapi.dependencies.models import Dependant
# from fastapi.routing import get_request_handler
from pydantic import BaseModel
from pydantic.v1.utils import lenient_issubclass
from starlette.routing import Router, Route, request_response

from fastapi1.applications.utils import get_path_param_names, get_param_field
from fastapi1.dependencies.models import Dependant


class APIRouter(Router):
    def __init__(self) -> None:
        super().__init__()
        self.route_class = APIRoute

    def add_api_route(self, path: str, endpoint: Callable[..., Any], method: str) -> None:
        route = self.route_class(
            path,
            endpoint=endpoint,
            method=method,
        )
        self.routes.append(route)

    def get(self, path: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: [Callable[..., Any]]) -> [Callable[..., Any]]:
            self.add_api_route(path, func, method='get')
            return func

        return decorator

    def post(self, path: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: [Callable[..., Any]]) -> [Callable[..., Any]]:
            self.add_api_route(path, func, method='post')
            return func

        return decorator


class APIRoute(Route):
    def __init__(self, path: str, endpoint: Callable[..., Any], method: str) -> None:
        self.path = path
        self.endpoint = endpoint
        self.method = method
        assert callable(endpoint), "Endpoint must be callable"
        self.dependant = get_dependant(
            path=self.path,
            call=self.endpoint
        )
        self.app = request_response(get_request_handler(dependant=self.dependant))


def get_dependant(*, path: str, call: Callable[..., Any]) -> Dependant:
    path_param_names = get_path_param_names(path)
    endpoint_signature = inspect.signature(call)
    signature_params = endpoint_signature.parameters
    dependant = Dependant(call=call, path=path)
    for param_name, param in signature_params.items():
        param_field = get_param_field(
            param=param,
            param_name=param_name
        )
        if param_name in path_param_names:
            dependant.path_params.append(param_field)
        elif (lenient_issubclass(param_field.type_, (list, set, tuple, dict)) or
              lenient_issubclass(param_field.type_, BaseModel)
        ):
            dependant.body_params.append(param_field)
        else:
            dependant.query_params.append(param_field)

    return dependant


def get_request_handler(dependant: Dependant, ) -> Callable[[Request], Coroutine[Any, Any, Response]]:
    is_coroutine = asyncio.iscoroutinefunction(dependant.call)
    async def app(request: Request) -> Response:
	  body = None
        if dependant.body_params:
            body = await request.json()
            буду
      solved_result = await solve_dependencies(
            request=request,
            dependant=dependant,
            body=body
            )
        values, errors = solved_result
        if errors: raise ValidationError(errors, RequestErrorModel)

        raw_response = await run_endpoint_function(
                dependant=dependant, values=values, is_coroutine=is_coroutine
            )
        if isinstance(raw_response, Response): return raw_response
	  if isinstance(raw_response, (dict, str, int, float, type(None))):
            return JSONResponse(raw_response)
        else: raise Exception("Type of response is not supported yet.")

    return app
