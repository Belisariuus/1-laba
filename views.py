""" Django views module. """
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .forms import LayerUploadForm
from .models import MapLayer


def update_layers(request: HttpRequest):
    """
    Обновляет состояние слоёв (включены/выключены) на основе данных формы.

    Args:
        request: HTTP-запрос с данными формы.
    Returns:
        Redirect: Перенаправление обратно на карту.
    """

    if request.method == "POST":
        all_layers = MapLayer.objects.all()
        all_layers.update(is_active=False)

        for layer in all_layers:
            if f"layer_{layer.id}" in request.POST:
                layer.is_active = True
                layer.save()

    return redirect("city_map")


def city_map(request: HttpRequest) -> HttpResponse:
    """
        Отображает карту с формой для загрузки и списком слоёв.

        Args:
            request: Объект HTTP-запроса.

        Returns:
            HttpResponse: Ответ с шаблоном city_map.html
    """
    if request.method == 'POST':
        form = LayerUploadForm(request.POST, request.FILES)
        if form.is_valid():
            layer = MapLayer(
                name=form.cleaned_data['layer_name'],
                layer_type=form.cleaned_data['layer_type'],
                csv_file=form.cleaned_data['layer_file']
            )
            layer.save()
            return redirect('city_map')
    else:
        form = LayerUploadForm()

    layers = MapLayer.objects.all()
    active_layers = [layer for layer in layers if layer.is_active]

    return render(request, "city_map.html", {
        "form": form,
        "layers": layers,
        "active_layers_data": [layer.get_processed_data() for layer in active_layers]
    })











import json
from .forms import RouteForm
from .ride_utils import pfa
from django.http import HttpResponseRedirect
from .modules import find_nodes
from .modules import context_timer as ct
from .ride_utils import dijkstra_pfa as pfa
    # print("Инициализация...")
    #
    # form_route = RouteForm()
    # layers_data = []
    # map_data = {
    #     "layers_data": layers_data,
    # }
    #
    # context = {
    #     "form_route": form_route,
    #     "map_data": json.dumps(map_data),
    #     "csv_error_message": "",
    # }
    # # Check Layers
    # if request.method == "POST":
    #
    #     # if 'route' in request.POST:
    #     #     form_route = RouteForm(request.POST)
    #     #     if form_route.is_valid():
    #     #         start_lat = form_route.cleaned_data['start_latitude']
    #     #         start_lon = form_route.cleaned_data['start_longitude']
    #     #         end_lat = form_route.cleaned_data['end_latitude']
    #     #         end_lon = form_route.cleaned_data['end_longitude']
    #     #         print(start_lat, start_lon, end_lat, end_lon)
    #     #
    #     #         # Поиск ближайших нод графа для начала и окончания движения
    #     #         # start_node = find_nodes.find_nearest_node(graph, start_lat, start_lon)[0]
    #     #         # end_node = find_nodes.find_nearest_node(graph, end_lat, end_lon)[0]
    #     #         # print("NODES: ", start_node, end_node)
    #     #         # # Инициализируем объект класса Дейкстра
    #     #         # dijkstra_algo = pfa.Dijkstra(graph)
    #     #         """
    #     #         Функция вычисляет точки маршрута
    #     #         route_path - список всех/промежуточных точек маршрута
    #     #         route_lenth - длина маршрута в метрах
    #     #         """
    #     #         # try:
    #     #         #     with ct.timer() as elapsed_time:
    #     #         #         route_lenth, route_path = dijkstra_algo.find_path(start_node, end_node)
    #     #         #     print("Маршрут найден")
    #     #         #     route_path = str(route_path).replace("(", "[").replace(")", "]")
    #     #         #     return render(request, "city_map.html", context={'route_points': route_path})
    #     #         # except:
    #     #         #     raise "Ошибка при построении маршрута!"
    #     #         #     return render(request, "city_map.html")
    #     #
    #
    #     else:
    #         print('1')
    #
    #         return HttpResponseRedirect(request.path_info)


