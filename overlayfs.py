from yum.plugins import TYPE_CORE
from os import utime, walk, path

requires_api_version = '2.3'
plugin_type = (TYPE_CORE,)
base_dir = 'var/lib/rpm/'
mtab = '/etc/mtab'

def should_touch():
        """ 
        Touch the files only once we've verified that
        we're on overlay mount
        """
        with open(mtab, 'r') as f:
                line = f.readline()
                return line and line.startswith('overlay /')
        return False

def init_hook(conduit):
        if not should_touch():
                return
	ir = conduit.getConf().installroot
        try:
                for root, _, files in walk(path.join(ir, base_dir)):
                        for f in files:
                                p = path.join(root, f)
                                with open(p, 'a'):
                                        utime(p, None)
        except Exception as e:
                conduit.error(1, "Error while doing RPMdb copy-up:\n%s" % e)
