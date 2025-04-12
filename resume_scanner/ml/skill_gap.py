import re

COURSE_RECOMMENDATIONS = {
    'python': [
        'https://www.udemy.com/course/python-for-beginners/',
        'https://nptel.ac.in/courses/106/106/106106145/',
        'https://www.youtube.com/watch?v=_uQrJ0TkZlc'
    ],
    'java': [
        'https://www.udemy.com/course/java-the-complete-java-developer-course/',
        'https://nptel.ac.in/courses/106/105/106105191/',
        'https://www.youtube.com/watch?v=ntLJmHOJ0ME'
    ],
    'django': [
        'https://www.udemy.com/course/python-and-django-full-stack-web-developer-bootcamp/',
        'https://www.youtube.com/watch?v=F5mRW0jo-U4'
    ],
    'mongodb': [
        'https://www.udemy.com/course/mongodb-the-complete-developers-guide/',
        'https://www.youtube.com/watch?v=-56x56UppqQ'
    ],
    'mern': [
        'https://www.udemy.com/course/mern-stack-front-to-back/',
        'https://www.youtube.com/watch?v=4ZzdTLaP6H4'
    ],
    'docker': [
        'https://www.udemy.com/course/docker-mastery/',
        'https://nptel.ac.in/courses/106/106/106106228/',
        'https://www.youtube.com/watch?v=fqMOX6JJhGo'
    ],
    'sql': [
        'https://www.coursera.org/learn/sql-for-data-science',
        'https://www.youtube.com/watch?v=27axs9dO7AE'
    ],
    'tableau': [
        'https://www.udemy.com/course/tableau10/',
        'https://www.youtube.com/watch?v=puBgaG0nTh4'
    ],
    'excel': [
        'https://www.coursera.org/learn/excel-essentials',
        'https://www.youtube.com/watch?v=8Xg4lJx5aJc'
    ],
    'machine learning': [
        'https://www.coursera.org/learn/machine-learning',
        'https://www.youtube.com/watch?v=Gv9_4yMHFhI',
        'https://nptel.ac.in/courses/106/106/106106202/'
    ],
"ethical_hacking": [
    "https://www.eccouncil.org/programs/certified-ethical-hacker-ceh/",
    "https://www.hackthebox.com/"
],
"tryhackme": [
    "https://tryhackme.com/",
    "https://www.youtube.com/playlist?list=PLBf0hzazHTGMomugG-8Y73D7XWkm2Bl-7"
],
"firewalls": [
    "https://www.cloudflare.com/learning/ddos/glossary/firewall/",
    "https://www.ibm.com/docs/en/i/7.4?topic=protection-firewalls"
],
"siem": [
    "https://www.splunk.com/en_us/resources/what-is-siem.html",
    "https://www.coursera.org/learn/siem"
],
"bash": [
    "https://ryanstutorials.net/bash-scripting-tutorial/",
    "https://linuxconfig.org/bash-scripting-tutorial-for-beginners"
],
"python_security": [
    "https://owasp.org/www-project-top-ten/",
    "https://www.udemy.com/course/python-for-cybersecurity/"
],
    "ci_cd": [
    "https://www.atlassian.com/continuous-delivery/ci-vs-cd",
    "https://www.jenkins.io/doc/"
],
"docker": [
    "https://docker-curriculum.com/",
    "https://docs.docker.com/get-started/"
],
"kubernetes": [
    "https://kubernetes.io/docs/tutorials/kubernetes-basics/",
    "https://www.udemy.com/course/learn-kubernetes/"
],
"jenkins": [
    "https://www.jenkins.io/doc/pipeline/tour/getting-started/",
    "https://www.udemy.com/course/jenkins-pipeline-step-by-step/"
],
"aws_gcp": [
    "https://aws.amazon.com/training/",
    "https://cloud.google.com/training"
],
"bash_scripting": [
    "https://linuxconfig.org/bash-scripting-tutorial-for-beginners",
    "https://www.shellscript.sh/"
],
    "aws": [
    "https://aws.amazon.com/training/",
    "https://www.udemy.com/course/aws-certified-cloud-practitioner/"
],
"azure": [
    "https://learn.microsoft.com/en-us/training/azure/",
    "https://www.udemy.com/course/70532-azure/"
],
"gcp": [
    "https://cloud.google.com/training",
    "https://www.coursera.org/learn/gcp-fundamentals"
],
"cloud_architecture": [
    "https://www.coursera.org/specializations/cloud-architecture",
    "https://learn.microsoft.com/en-us/azure/architecture/"
],
"load_balancing": [
    "https://cloud.google.com/load-balancing/docs",
    "https://aws.amazon.com/elasticloadbalancing/"
],
"virtual_machines": [
    "https://azure.microsoft.com/en-in/resources/virtual-machines/",
    "https://www.ibm.com/cloud/learn/virtual-machines"
],
    "requirement_gathering": [
        "https://www.tutorialspoint.com/requirement_gathering",
        "https://www.udemy.com/course/business-analysis-fundamentals/"
    ],
    "stakeholder_communication": [
        "https://www.coursera.org/learn/business-communication",
        "https://www.linkedin.com/learning/communications-for-business-professionals"
    ],
    "data_analysis_excel": [
        "https://www.coursera.org/specializations/excel",
        "https://exceljet.net/"
    ],
    "sql_reporting": [
        "https://www.sqltutorial.org/",
        "https://mode.com/sql-tutorial/"
    ],
    "python_backend": [
    "https://realpython.com/tutorials/django/",
    "https://flask.palletsprojects.com/en/2.2.x/tutorial/"
],
"java_spring": [
    "https://spring.io/guides",
    "https://www.udemy.com/course/spring-framework-tutorial-for-beginners/"
],
"nodejs_backend": [
    "https://nodejs.dev/en/learn/",
    "https://developer.mozilla.org/en-US/docs/Learn/Server-side/Express_Nodejs"
],
"sql_nosql": [
    "https://www.w3schools.com/sql/",
    "https://www.mongodb.com/basics"
],
"figma": [
    "https://www.figma.com/resources/learn-design/",
    "https://www.youtube.com/watch?v=FTFaQWZBqQ8"
],
"adobe_xd": [
    "https://helpx.adobe.com/xd/tutorials.html",
    "https://www.udemy.com/course/user-experience-design-adobe-xd/"
],
"sketch": [
    "https://www.sketch.com/learn/",
    "https://www.udemy.com/course/sketch-app/"
],
"html_css": [
    "https://developer.mozilla.org/en-US/docs/Learn/HTML",
    "https://developer.mozilla.org/en-US/docs/Learn/CSS"
],
"user_journey_mapping": [
    "https://careerfoundry.com/en/blog/ux-design/user-journey-maps/",
    "https://www.uxpin.com/studio/blog/user-journey-map-template/"
],
"usability_testing": [
    "https://www.nngroup.com/articles/usability-testing-101/",
    "https://www.interaction-design.org/courses/usability-testing"
]

}

def analyze_skill_gap(resume_text, job_description):
    """
    Analyze skill gaps based on keywords in the job description that are missing
    or insufficiently represented in the resume.
    """
    if not resume_text or not job_description:
        return {}

    resume_text = resume_text.lower()
    job_description = job_description.lower()
    skill_links = {}

    for skill, links in COURSE_RECOMMENDATIONS.items():
        if skill in job_description and skill not in resume_text:
            skill_links[skill] = links

    return skill_links
