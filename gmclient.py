import requests
import json

class GMClient(object):
    headers = {'content-type': 'application/json'}
    host = ''
    session_token = ''
    last_error = ''
    resolver_cache = {}

    URLS = {
        'login': '/api/auth/login/',
        'logout': '/api/auth/logout/',
        'projects': '/api/scrum/projects/',
        'project': '/api/scrum/projects/%d/',
        'milestones': '/api/scrum/milestones/',
        'milestone': '/api/scrum/milestones/%d/',
        'user_stories': '/api/scrum/user_stories/',
        'user_story': '/api/scrum/user_stories/%d/',
        'tasks': '/api/scrum/tasks/',
        'task': '/api/scrum/tasks/%d/',
        'issues': '/api/scrum/issues/',
        'issue': '/api/scrum/issues/%d/',
        'questions': '/api/scrum/questions/',
        'question': '/api/scrum/questions/%d/',
        'documents': '/api/scrum/documents/',
        'document': '/api/scrum/documents/%d/',
        'issue_types': '/api/scrum/issue_types/',
        'issue_status': '/api/scrum/issue_status/',
        'task_status': '/api/scrum/task_status/',
        'user_story_status': '/api/scrum/user_story_status/',
        'severities': '/api/scrum/severities/',
        'priorities': '/api/scrum/priorities/',
        'points': '/api/scrum/points/',
    }

    def resolve(self, project_id, choice_type, value):
        value = self.resolver_cache.get(project_id, {}).get(choice_type, {}).get(value, '')
        if not value:
            headers = self.headers
            headers['X-Session-Token'] = self.session_token
            params = { "project": project_id }
            response = requests.get(self.host+self.URLS.get(choice_type), params=params, headers=headers)
            if response.status_code == 200:
                if project_id not in self.resolver_cache:
                    self.resolver_cache[project_id] = {}
                if choice_type not in self.resolver_cache.get(project_id):
                    self.resolver_cache[project_id][choice_type] = {}
                for choice in json.loads(response.content):
                    self.resolver_cache[project_id][choice_type][choice.get('id', '')] = choice.get('name', '')
            else:
                value = ''

        return value

    def login(self, host, username, password):
        login_data = {
            'username': username,
            'password': password,
        }
        response = requests.post(host+self.URLS.get('login'), data=json.dumps(login_data), headers=self.headers)

        if response.status_code == 200:
            data = json.loads(response.content)
            self.session_token = data.get('token', '')
            self.host = host
            return True
        elif response.status_code == 400:
            data = json.loads(response.content)
            self.last_error = data.get('detail', '')
            return False

    def list_projects(self):
        headers = self.headers
        headers['X-Session-Token'] = self.session_token
        response = requests.get(self.host+self.URLS.get('projects'), headers=headers)

        if response.status_code == 200:
            data = json.loads(response.content)
            return data
        elif response.status_code == 400:
            data = json.loads(response.content)
            self.last_error = data.get('detail', '')
            return None

    def get_project(self, project_id):
        headers = self.headers
        headers['X-Session-Token'] = self.session_token
        response = requests.get(self.host+self.URLS.get('project') % int(project_id), headers=headers)

        if response.status_code == 200:
            data = json.loads(response.content)
            return data
        elif response.status_code == 400:
            data = json.loads(response.content)
            self.last_error = data.get('detail', '')
            return None

    def list_milestones(self, project=None):
        headers = self.headers
        headers['X-Session-Token'] = self.session_token

        params = {}
        if project:
            params = { "project": project }

        response = requests.get(self.host+self.URLS.get('milestones'), params=params, headers=headers)

        if response.status_code == 200:
            data = json.loads(response.content)
            return data
        elif response.status_code == 400:
            data = json.loads(response.content)
            self.last_error = data.get('detail', '')
            return None

    def get_milestone(self, milestone_id):
        headers = self.headers
        headers['X-Session-Token'] = self.session_token
        response = requests.get(self.host+self.URLS.get('milestone') % int(milestone_id), headers=headers)

        if response.status_code == 200:
            data = json.loads(response.content)
            return data
        elif response.status_code == 400:
            data = json.loads(response.content)
            self.last_error = data.get('detail', '')
            return None


    def list_user_stories(self, project=None, milestone=None):
        headers = self.headers
        headers['X-Session-Token'] = self.session_token

        params = {}
        if milestone:
            params = { "milestone": milestone }
        elif project:
            params = { "project": project }

        response = requests.get(self.host+self.URLS.get('user_stories'), params=params, headers=headers)

        if response.status_code == 200:
            data = json.loads(response.content)
            return data
        elif response.status_code == 400:
            data = json.loads(response.content)
            self.last_error = data.get('detail', '')
            return None

    def get_user_story(self, user_story_id):
        headers = self.headers
        headers['X-Session-Token'] = self.session_token
        response = requests.get(self.host+self.URLS.get('user_story') % int(user_story_id), headers=headers)

        if response.status_code == 200:
            data = json.loads(response.content)
            return data
        elif response.status_code == 400:
            data = json.loads(response.content)
            self.last_error = data.get('detail', '')
            return None

    def list_tasks(self, project=None, milestone=None, user_story=None):
        headers = self.headers
        headers['X-Session-Token'] = self.session_token

        params = {}
        if user_story:
            params = { "user_story": user_story }
        elif milestone:
            params = { "milestone": milestone }
        elif project:
            params = { "project": project }

        response = requests.get(self.host+self.URLS.get('tasks'), params=params, headers=headers)

        if response.status_code == 200:
            data = json.loads(response.content)
            return data
        elif response.status_code == 400:
            data = json.loads(response.content)
            self.last_error = data.get('detail', '')
            return None

    def get_task(self, task_id):
        headers = self.headers
        headers['X-Session-Token'] = self.session_token
        response = requests.get(self.host+self.URLS.get('task') % int(task_id), headers=headers)

        if response.status_code == 200:
            data = json.loads(response.content)
            return data
        elif response.status_code == 400:
            data = json.loads(response.content)
            self.last_error = data.get('detail', '')
            return None

    def list_issues(self, project=None):
        headers = self.headers
        headers['X-Session-Token'] = self.session_token

        params = {}
        if project:
            params = { "project": project }

        response = requests.get(self.host+self.URLS.get('issues'), params=params, headers=headers)

        if response.status_code == 200:
            data = json.loads(response.content)
            return data
        elif response.status_code == 400:
            data = json.loads(response.content)
            self.last_error = data.get('detail', '')
            return None

    def get_issue(self, issue_id):
        headers = self.headers
        headers['X-Session-Token'] = self.session_token
        response = requests.get(self.host+self.URLS.get('issue') % int(issue_id), headers=headers)

        if response.status_code == 200:
            data = json.loads(response.content)
            return data
        elif response.status_code == 400:
            data = json.loads(response.content)
            self.last_error = data.get('detail', '')
            return None

    def list_questions(self, project=None):
        headers = self.headers
        headers['X-Session-Token'] = self.session_token

        params = {}
        if project:
            params = { "project": project }

        response = requests.get(self.host+self.URLS.get('questions'), params=params, headers=headers)

        if response.status_code == 200:
            data = json.loads(response.content)
            return data
        elif response.status_code == 400:
            data = json.loads(response.content)
            self.last_error = data.get('detail', '')
            return None

    def get_question(self, question_id):
        headers = self.headers
        headers['X-Session-Token'] = self.session_token
        response = requests.get(self.host+self.URLS.get('question') % int(question_id), headers=headers)

        if response.status_code == 200:
            data = json.loads(response.content)
            return data
        elif response.status_code == 400:
            data = json.loads(response.content)
            self.last_error = data.get('detail', '')
            return None

    def list_documents(self, project=None):
        headers = self.headers
        headers['X-Session-Token'] = self.session_token

        params = {}
        if project:
            params = { "project": project }

        response = requests.get(self.host+self.URLS.get('documents'), params=params, headers=headers)

        if response.status_code == 200:
            data = json.loads(response.content)
            return data
        elif response.status_code == 400:
            data = json.loads(response.content)
            self.last_error = data.get('detail', '')
            return None

    def get_document(self, document_id):
        headers = self.headers
        headers['X-Session-Token'] = self.session_token
        response = requests.get(self.host+self.URLS.get('document') % int(document_id), headers=headers)

        if response.status_code == 200:
            data = json.loads(response.content)
            return data
        elif response.status_code == 400:
            data = json.loads(response.content)
            self.last_error = data.get('detail', '')
            return None
