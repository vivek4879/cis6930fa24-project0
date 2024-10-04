import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from project0.extractingincidents import clean_data

def test_clean_data():
    test_line = ['                                                                                                                        Daily Incident Summary (Public)', '            Date / Time                           Incident Number                                                        Location                                                                                       Nature                                                       Incident ORI', '9/25/2024 0:03                                2024-00069985                        1186 E ROCK CREEK RD                                                                        Traffic Stop                                                                                   OK0140200']
    required_output = [['9/25/2024 0:03', '2024-00069985', '1186 E ROCK CREEK RD', 'Traffic Stop', 'OK0140200']]
    our_output = clean_data(test_line)
    assert our_output == required_output