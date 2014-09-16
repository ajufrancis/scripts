vm_count = ''

cpu_number = [
  '1',
  '2',
  '4',
  '6',
  '8',
  '16',
]
#GB
disk_size = [
  '10',
  '20',
  '50',
  '80',
  '100',
  '200',
  '300',
  '500',
  'custom',
]

#GB
mem_size = [
  '1',
  '2',
  '4',
  '8',
  '16',
  'custom',
]

os = {
  'windows': {
    'wxp3': ['i386'],
    'w2k3r2': ['i386', 'x86_64'],
    'w2k8r2': ['x86_64']
  },
  'linux': {
    'centos': {
      '5': ['i386', 'x86_64'],
      '6': ['i386', 'x86_64']
    },
    'rhel': {
      '5': ['i386', 'x86_64'],
      '6': ['i386', 'x86_64']
    },
    'ubuntu': {
      'lucid': ['i386', 'x86_64'],
      'precise': ['i386', 'x86_64']
    }
  }
}

os_role = {
  'login': ['vnc', 'rdp', 'ssh']
}

net = {
  'vpn': ['yes', 'no'],
  'isp': ['cnc', 'ctc'],
  'wan': ['yes', 'no'],
}

sysconfig = {
  'fw': 'no'
  'selinux': 'no'
}
