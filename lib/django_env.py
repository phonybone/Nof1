import os, sys
django_root=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'www', 'Nof1'))
sys.path.append(django_root)
os.environ['DJANGO_SETTINGS_MODULE']='Nof1.settings'

