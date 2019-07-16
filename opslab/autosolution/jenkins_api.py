import os

import jenkins

jenkins_url = "http://10.6.5.100:8000/"
jenkins_username = "dh_ci01"
jenkins_password = "11c54ff558ab312fc5f20758f0c34659cb"

def trigger_job(build_url, receivers, stage, mode):
    """
    For example:
        >>> import jenkins
        >>> jenkins_url = "http://10.6.5.100:8000/"
        >>> jenkins_username = "dh_ci01"
        >>> jenkins_password = "11c54ff558ab312fc5f20758f0c34659cb"
        >>> server = jenkins.Jenkins(jenkins_url, username=jenkins_username, password=jenkins_password)
        >>> name = "trigger-autosolution"
        >>> parameters = {'target_build_url': 'http://10.6.5.99:8000/job/Proj_SsmsSaas--linux-centos-gcc/128/', 'receivers': '45128', 'mode': "test"}
        >>> server.build_job(name, parameters)
    """
    server = jenkins.Jenkins(jenkins_url, username=jenkins_username, password=jenkins_password)
    name = "trigger-autosolution"
    parameters = {
        'target_build_url': build_url,
        'receivers': receivers,
        'stage': stage,
        'mode': mode
    }

    # 不允许存在代理，否则调用Jenkins接口会出现403
    if 'http_proxy' in os.environ:
        del os.environ['http_proxy']
    if 'https_proxy' in os.environ:
        del os.environ['https_proxy']
    result = server.build_job(name, parameters)
