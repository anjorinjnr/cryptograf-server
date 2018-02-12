import sys
import os
import subprocess


def run_unit_test():
  sdk_path = '/Users/eanjorin/google-cloud-sdk/platform/google_appengine'
  try:
    subprocess.check_output(['python', 'runner.py', sdk_path],
                            stderr=subprocess.STDOUT)
  except subprocess.CalledProcessError as  e:
    return 'Presubmit failed due to failing tests: %s' % e.output

  return 0


if __name__ == "__main__":
  sys.exit(run_unit_test(), True)