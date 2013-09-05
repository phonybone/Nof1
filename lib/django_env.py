import os, sys
django_root=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'www', 'Nof1'))
print 'django_root is %s' % django_root
sys.path.append(django_root)
import django

os.environ['DJANGO_SETTINGS_MODULE']='Nof1.settings'

