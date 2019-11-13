from django.http import JsonResponse
import json, os
import yaml
from mock.settings import BASE_DIR

api_file = os.path.join(BASE_DIR, 'api_file')
map_list = {}


def get_api_file_name(path):
    """
    获取接口文件名
    :param path:
    :return:
    """
    listName = []
    for fileName in os.listdir(path):
        if os.path.splitext(fileName)[1] == '.yaml':
            fileName = os.path.splitext(fileName)[0]
            listName.append(fileName)
    return listName


def save_api(name, body):
    """
    保存接口yaml文件
    :param name: 接口路径
    :param body: 返回数据
    :return:
    """
    # file_paht = api_file + '/' + name + '.yaml'
    file_paht = os.path.join(api_file, '%s.yaml' % name)
    f = open(file_paht, 'w', encoding='utf8')
    yaml.dump(body, f)
    f.close()


def open_api_file(name):
    """
    读取配置文件
    :param name:
    :return:
    """
    try:
        # file_paht = api_file + '/' + name + '.yaml'
        file_paht = os.path.join(api_file,'%s.yaml'%name)
        f = open(file_paht, 'r', encoding="utf8")
        data = yaml.load(f)
        return data
    except Exception as e:
        data = {
            "msg": "当前接口不存在"
        }
        return data


def read_map():
    api_name_list = get_api_file_name(api_file)
    for i in api_name_list:
        file_body = open_api_file(i)
        map_list[i] = file_body
    return map_list


def add_api(request):
    if request.method == "POST":
        body_data = request.body
        data = json.loads(body_data)
        api_name = data.get("name", None)
        body = data.get("body", None)
        config = data.get("config", None)
        data["url"] = "/api/%s" % api_name
        if api_name and body and config:
            save_api(api_name, data)
            read_map()
            return JsonResponse({"code": 1, "msg": "新增成功", "body": data})
        else:
            return JsonResponse({"code": -1, "msg": "缺少name，body，或者config"})
    elif request.method == "GET":
        data = request.GET.dict()
        api_name = data.get('name')
        data.pop('name')
        data["url"] = "/api/%s" % api_name
        if api_name and data:
            save_api(api_name, data)
            read_map()
            return JsonResponse({"code": 1, "msg": "新增成功", "body": data})
        else:
            return JsonResponse({"code": -1, "msg": "缺少name，body，或者config"})
    else:
        return JsonResponse({"cdoe": 5000, "msg": '请用POST请求'})


def api(request, path):
    if not map_list:
        read_map()
    if path not in map_list.keys():
        return JsonResponse({"code":5001,"msg":"当前接口不存在"})

    if request.method == "POST":
        # data_body = request.body
        # data = json.loads(data_body)
        # body_config_list = data.keys()
        file_body = map_list[path]['body']
        # api_config_list = map_list[path]['config'].keys()
        # Difference_value = [y for y in api_config_list if y not in body_config_list]
        # if not Difference_value:
        return JsonResponse(file_body)
    # else:
    #     return JsonResponse({"msg": '缺少参数%s' % Difference_value})

    elif request.method == "GET":
        # body_config_list = request.GET.keys()
        file_body = dict.copy(map_list[path])
        file_body.pop('url')
        # api_config_list = file_body.keys()
        # Difference_value = [y for y in api_config_list if y not in body_config_list]
        # if not Difference_value:
        return JsonResponse(file_body)
        # else:
        #     return JsonResponse({"msg": '缺少参数%s' % Difference_value})
    else:
        return JsonResponse({"cdoe": 5000, "msg": '请用POST,或GET请求'})
