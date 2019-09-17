from abc import abstractmethod

import utils


class ApiAdapter:
    @abstractmethod
    def clone_course(self, path, id):
        pass

    @abstractmethod
    def clone_module(self, path, id):
        pass

    @abstractmethod
    def clone_lesson(self, path, id):
        pass

    @abstractmethod
    def clone_task(self, path, id):
        pass



# Run with Python 3
# Saves all step sources into foldered structure
import os
import json
import requests
import datetime


class StepikAdapter(ApiAdapter):
    client_id = -1
    client_secret = -1
    api_host = 'https://stepik.org'
    token = ""

    ###################
    # Adapter methods
    ###################

    def __init__(self, client_id, client_secret):
        self.get_token(client_id, client_secret)

    def get_token(self, client_id, client_secret):
        auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
        response = requests.post(self.api_host + '/oauth2/token/',
                                 data={'grant_type': 'client_credentials'},
                                 auth=auth)
        token = response.json().get('access_token', None)
        if not token:
            raise Exception('Unable to authorize with provided credentials')
        self.token = token

    def clone_course(self, path, id):
        course = self.fetch_object('course', id)

        new_path = os.path.join(path, "{} {}".format(course['id'], course['title']))
        os.mkdir(new_path)

        for section_id in course['sections']:
            self.clone_module(new_path, section_id)

    def clone_module(self, path, id):
        section = self.fetch_object('section', id)

        new_path = os.path.join(path, "{} {}".format(section['position'], section['title']))
        os.mkdir(new_path)

        for unit_id in section['units']:
            self.clone_lesson(new_path, unit_id)

    def clone_lesson(self, path, id):
        unite = self.fetch_object('unit', id)
        lesson_id = unite['lesson']
        lesson = self.fetch_object('lesson', lesson_id)

        new_path = os.path.join(path, "{} {}".format(unite['position'], lesson['title']))
        os.mkdir(new_path)

        for idx, step_id in enumerate(lesson['steps']):
            self.clone_task(new_path, step_id)

    def clone_task(self, path, id):
        step = self.fetch_object('step', id)
        step_source = self.fetch_object('step-source', step['id'])

        new_path = os.path.join(path, str(step['position']))
        os.mkdir(new_path)

        filename = os.path.join(new_path, 'data.json')
        data = {
            'block': step_source['block'],
            'id': str(step['id']),
            'time': datetime.datetime.now().isoformat()
        }
        utils.write_json(filename, data)

    ###########
    # Private
    ###########

    def fetch_object(self, obj_class, obj_id):
        api_url = '{}/api/{}s/{}'.format(self.api_host, obj_class, obj_id)
        response = requests.get(api_url, headers={'Authorization': 'Bearer ' + self.token}).json()
        return response['{}s'.format(obj_class)][0]

    def fetch_objects(self, obj_class, obj_ids):
        objs = []
        # Fetch objects by 30 items,
        # so we won't bump into HTTP request length limits
        step_size = 30
        for i in range(0, len(obj_ids), step_size):
            obj_ids_slice = obj_ids[i:i + step_size]
            api_url = '{}/api/{}s?{}'.format(self.api_host, obj_class,
                                             '&'.join('ids[]={}'.format(obj_id)
                                                      for obj_id in obj_ids_slice))
            response = requests.get(api_url,
                                    headers={'Authorization': 'Bearer ' + self.token}
                                    ).json()
            objs += response['{}s'.format(obj_class)]
        return objs
