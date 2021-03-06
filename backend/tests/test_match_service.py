from flask import g

from court.database import db
from court.users.auth_service import AuthService, AuthorizationError
from court.matches.match_service import MatchService
from court.users.models import User, Profile

import pytest

def test_get_current_matches(app):
  with app.app_context():
    g.user_id = '3'
    auth_service = AuthService('secret', None, None)
    match_service = MatchService()
    no_matches = match_service.get_current_matches()
    assert no_matches == {}

  with app.app_context():
    g.user_id = '1'
    auth_service = AuthService('secret', None, None)
    match_service = MatchService()
    matches = match_service.get_current_matches()

    mock_matches = {
      '2': {
        'active': True,
        'percent_unlocked': 0,
        'profile': {
          'animal': '',
          'color': '',
          'gender': '',
          'preferred_gender': '',
          'first_name': '',
          'last_name': '',
          'profile_picture': '',
          'interests': {}
        }
      }
    }

    assert matches == mock_matches

def test_inactivate_match_1(app):
  with app.app_context():
    g.user_id = '1'
    auth_service = AuthService('secret', None, None)
    match_service = MatchService()

    # Check user 2 is as an active match for user 1
    mock_matches_1 = {
      '2': {
        'active': True,
        'percent_unlocked': 0,
        'profile': {
          'animal': '',
          'color': '',
          'gender': '',
          'preferred_gender': '',
          'first_name': '',
          'last_name': '',
          'profile_picture': '',
          'interests': {}
        }
      }
    }
    matches_for_1 = match_service.get_current_matches()
    assert matches_for_1 == mock_matches_1

    # Check user 1 is as an active match for user 2
    g.user_id = '2'
    mock_matches_2 = {
      '1': {
        'active': True,
        'percent_unlocked': 0,
        'profile': {
          'animal': '',
          'color': '',
          'gender': '',
          'preferred_gender': '',
          'first_name': '',
          'last_name': '',
          'profile_picture': '',
          'interests': {}
        }
      }
    }
    matches_for_2 = match_service.get_current_matches()
    assert matches_for_2 == mock_matches_2
    g.user_id = '1'

    match_deleted = match_service.inactivate_match(2)
    assert match_deleted == True

    # Since both users only have one match each, they should no longer have any
    matches_for_1 = match_service.get_current_matches()
    assert matches_for_1 == {}
    g.user_id = '2'
    matches_for_2 = match_service.get_current_matches()
    assert matches_for_2 == {}

def test_inactivate_match_2(app):
  with app.app_context():
    g.user_id = '1'
    auth_service = AuthService('secret', None, None)
    match_service = MatchService()

    # Check user 2 is as an active match for user 1
    mock_matches_1 = {
      '2': {
        'active': True,
        'percent_unlocked': 0,
        'profile': {
          'animal': '',
          'color': '',
          'gender': '',
          'preferred_gender': '',
          'first_name': '',
          'last_name': '',
          'profile_picture': '',
          'interests': {}
        }
      }
    }
    matches_for_1 = match_service.get_current_matches()
    assert matches_for_1 == mock_matches_1

    # Check user 1 is as an active match for user 2
    g.user_id = '2'
    mock_matches_2 = {
      '1': {
        'active': True,
        'percent_unlocked': 0,
        'profile': {
          'animal': '',
          'color': '',
          'gender': '',
          'preferred_gender': '',
          'first_name': '',
          'last_name': '',
          'profile_picture': '',
          'interests': {}
        }
      }
    }
    matches_for_2 = match_service.get_current_matches()
    assert matches_for_2 == mock_matches_2
    g.user_id = '1'

    match_deleted = match_service.inactivate_match(2, purge=True)
    assert match_deleted == True

    # Since both users only have one match each, they should no longer have any
    matches_for_1 = match_service.get_current_matches()
    assert matches_for_1 == {}
    g.user_id = '2'
    matches_for_2 = match_service.get_current_matches()
    assert matches_for_2 == {}

def test_inactivate_match_noop(app):
  with app.app_context():
    g.user_id = '1'
    auth_service = AuthService('secret', None, None)
    match_service = MatchService()

    # Check user 2 is as an active match for user 1
    mock_matches_1 = {
      '2': {
        'active': True,
        'percent_unlocked': 0,
        'profile': {
          'animal': '',
          'color': '',
          'gender': '',
          'preferred_gender': '',
          'first_name': '',
          'last_name': '',
          'profile_picture': '',
          'interests': {}
        }
      }
    }
    matches_for_1 = match_service.get_current_matches()
    assert matches_for_1 == mock_matches_1

    matched_deleted = match_service.inactivate_match(3)
    assert matched_deleted == False

    # Since user 3 is not a match for user 1, there is no change to matches
    matches_for_1 = match_service.get_current_matches()
    assert matches_for_1 == mock_matches_1

def test_add_match_to_profile(app):
  with app.app_context():
    g.user_id = '1'
    auth_service = AuthService('secret', None, None)
    match_service = MatchService()

    # Check user 1 and user 3 are currently not matched
    matches_for_1 = match_service.get_current_matches()
    assert '3' not in matches_for_1.keys()
    g.user_id = '3'
    matches_for_3 = match_service.get_current_matches()
    assert '1' not in matches_for_3.keys()
    g.user_id = '1'

    # Simulate match between user 1 and user 3 on interest
    matched_interest = { 'test_key': 'test_val' }
    created_match = match_service.add_match_to_profile(3, matched_interest)
    assert created_match == True

    # Check user 3 got added as an active match for user 1
    mock_matches_1 = {
      '3': {
        'active': True,
        'percent_unlocked': 25,
        'profile': {
          'animal': '',
          'color': '',
          'gender': 'Female',
          'preferred_gender': 'Male',
          'first_name': '',
          'last_name': '',
          'profile_picture': '',
          'interests': { 'test_key' : 'test_val' }
        }
      }
    }
    matches_for_1 = match_service.get_current_matches()
    assert len(matches_for_1) == 2
    assert matches_for_1['3'] == mock_matches_1['3']

    # Check user 1 got added as an active match for user 3
    mock_matches_3 = {
      '1': {
        'active': True,
        'percent_unlocked': 25,
        'profile': {
          'animal': '',
          'color': '',
          'gender': 'Male',
          'preferred_gender': 'Female',
          'first_name': '',
          'last_name': '',
          'profile_picture': '',
          'interests': { 'test_key' : 'test_val' }
        }
      }
    }
    g.user_id = '3'
    matches_for_3 = match_service.get_current_matches()
    assert len(matches_for_3) == 1
    assert matches_for_3['1'] == mock_matches_3['1']

def test_add_match_to_profile_with_duplicate_match(app):
  with app.app_context():
    g.user_id = '1'
    auth_service = AuthService('secret', None, None)
    match_service = MatchService()

    # Check user 1 and user 2 are currently matched
    matches_for_1 = match_service.get_current_matches()
    assert '2' in matches_for_1.keys()
    g.user_id = '2'
    matches_for_2 = match_service.get_current_matches()
    assert '1' in matches_for_2.keys()
    g.user_id = '1'

    # Simulate duplicate match between user 1 and user 2 on interest, should fail
    matched_interest = { 'test_key': 'test_val' }
    created_match = match_service.add_match_to_profile(2, matched_interest)
    assert created_match == False

    # Check user 2 did not get added as a duplicate match for user 1
    mock_matches_1 = {
      '2': {
        'active': True,
        'percent_unlocked': 0,
        'profile': {
          'animal': '',
          'color': '',
          'gender': '',
          'preferred_gender': '',
          'first_name': '',
          'last_name': '',
          'profile_picture': '',
          'interests': {}
        }
      }
    }
    matches_for_1 = match_service.get_current_matches()
    assert len(matches_for_1) == 1
    assert matches_for_1['2'] == mock_matches_1['2']

def test_unlock_next_profile_feature_1(app):
  with app.app_context():
    g.user_id = '1'
    auth_service = AuthService('secret', None, None)
    match_service = MatchService()

    # Check user 1 and user 2 are currently matched
    matches_for_1 = match_service.get_current_matches()
    assert '2' in matches_for_1.keys()
    g.user_id = '2'
    matches_for_2 = match_service.get_current_matches()
    assert '1' in matches_for_2.keys()
    g.user_id = '1'

    # Unlock next profile feature for user 1 and user 2
    #
    # Each user has 1 interest, so the unlocked percentage should be 25%
    # because they have not yet unlocked each other's first_name, last_name,
    # or profile_picture
    data = match_service.unlock_next_profile_feature(2)
    assert data['user_percent_unlocked'] == 25
    assert data['matched_user_percent_unlocked'] == 25

    # Check user 2's interest show in the active match for user 1
    mock_matches_1 = {
      '2': {
        'active': True,
        'percent_unlocked': 25,
        'profile': {
          'animal': '',
          'color': '',
          'gender': '',
          'preferred_gender': '',
          'first_name': '',
          'last_name': '',
          'profile_picture': '',
          'interests': {'interest2': 'value2'}
        }
      }
    }
    matches_for_1 = match_service.get_current_matches()
    assert matches_for_1['2'] == mock_matches_1['2']

    # Check user 1's interest show in the active match for user 2
    mock_matches_2 = {
      '1': {
        'active': True,
        'percent_unlocked': 25,
        'profile': {
          'animal': '',
          'color': '',
          'gender': '',
          'preferred_gender': '',
          'first_name': '',
          'last_name': '',
          'profile_picture': '',
          'interests': {'interest1': 'value1'}
        }
      }
    }
    g.user_id = '2'
    matches_for_2 = match_service.get_current_matches()
    assert matches_for_2['1'] == mock_matches_2['1']

def test_unlock_next_profile_feature_2(app):
  with app.app_context():
    g.user_id = '1'
    auth_service = AuthService('secret', None, None)
    match_service = MatchService()

    # Check user 1 and user 2 are currently matched
    matches_for_1 = match_service.get_current_matches()
    assert '2' in matches_for_1.keys()
    g.user_id = '2'
    matches_for_2 = match_service.get_current_matches()
    assert '1' in matches_for_2.keys()
    g.user_id = '1'

    # Unlock next two profile features for user 1 and user 2
    #
    # Each user has 1 interest, so the unlocked percentages should be 25% after
    # first unlock because they have not yet unlocked each other's first_name,
    # last_name, or profile_picture; after the second unlock, the unlocked
    # percentages should be 50%.
    data = match_service.unlock_next_profile_feature(2)
    assert data['user_percent_unlocked'] == 25
    assert data['matched_user_percent_unlocked'] == 25
    data = match_service.unlock_next_profile_feature(2)
    assert data['user_percent_unlocked'] == 50
    assert data['matched_user_percent_unlocked'] == 50

    # Check user 2's interest and first_name show in the active match for user 1
    mock_matches_1 = {
      '2': {
        'active': True,
        'percent_unlocked': 50,
        'profile': {
          'animal': '',
          'color': '',
          'gender': '',
          'preferred_gender': '',
          'first_name': 'Josephine',
          'last_name': '',
          'profile_picture': '',
          'interests': {'interest2': 'value2'}
        }
      }
    }
    matches_for_1 = match_service.get_current_matches()
    assert matches_for_1['2'] == mock_matches_1['2']

    # Check user 1's interest and first_name show in the active match for user 2
    mock_matches_2 = {
      '1': {
        'active': True,
        'percent_unlocked': 50,
        'profile': {
          'animal': '',
          'color': '',
          'gender': '',
          'preferred_gender': '',
          'first_name': 'Joe',
          'last_name': '',
          'profile_picture': '',
          'interests': {'interest1': 'value1'}
        }
      }
    }
    g.user_id = '2'
    matches_for_2 = match_service.get_current_matches()
    assert matches_for_2['1'] == mock_matches_2['1']

def test_find_match_1(app):
  with app.app_context():
    g.user_id = '3'
    auth_service = AuthService('secret')
    match_service = MatchService()

    # Check user 3 and user 4 are currently not matched
    matches_for_3 = match_service.get_current_matches()
    assert '4' not in matches_for_3.keys()
    g.user_id = '4'
    matches_for_4 = match_service.get_current_matches()
    assert '3' not in matches_for_4.keys()
    g.user_id = '3'

    # Check users 3 and 4 got matched on interest3
    find_match_for_3 = match_service.find_match(3, 1)
    match_result = (4, { 'interest3' : 'value3' })
    assert len(find_match_for_3) == 1
    assert match_result in find_match_for_3

    # Check user 4 got added as an active match for user 3
    matches_for_3 = match_service.get_current_matches()
    assert len(matches_for_3) == 1
    assert matches_for_3['4']['profile']['interests'] == { 'interest3' : 'value3' }

    # Check user 3 got added as an active match for user 4
    g.user_id = '4'
    matches_for_4 = match_service.get_current_matches()
    assert len(matches_for_4) == 1
    assert matches_for_4['3']['profile']['interests'] == { 'interest3' : 'value3' }

def test_find_match_2(app):
  with app.app_context():
    g.user_id = '3'
    auth_service = AuthService('secret')
    match_service = MatchService()

    # Check user 3 and users 1 and 4 are currently not matched
    matches_for_3 = match_service.get_current_matches()
    assert '1' not in matches_for_3.keys()
    assert '4' not in matches_for_3.keys()
    g.user_id = '4'
    matches_for_4 = match_service.get_current_matches()
    assert '3' not in matches_for_4.keys()
    g.user_id = '1'
    matches_for_1 = match_service.get_current_matches()
    assert '3' not in matches_for_1.keys()
    g.user_id = '3'

    find_match_for_3 = match_service.find_match(3, 2)
    assert len(find_match_for_3) == 2

    # Check users 1 and 4 got added as an active match for user 3
    # User 4 is matched based on the shared interest3
    # User 1 is matched even without common interests because it is the only
    # other user in the database satisying user 3's gender preferences
    matches_for_3 = match_service.get_current_matches()
    assert len(matches_for_3) == 2
    assert matches_for_3['4']['profile']['interests'] == { 'interest3' : 'value3' }
    assert matches_for_3['1']['profile']['interests'] == { '' : '' }

    # Check user 3 got added as an active match for user 4
    g.user_id = '4'
    matches_for_4 = match_service.get_current_matches()
    assert len(matches_for_4) == 1
    assert matches_for_4['3']['profile']['interests'] == { 'interest3' : 'value3' }

    # Check user 3 got added as an active match for user 1
    g.user_id = '1'
    matches_for_1 = match_service.get_current_matches()
    assert len(matches_for_1) == 2
    assert matches_for_1['3']['profile']['interests'] == { '' : '' }

def test_find_match_3(app):
  with app.app_context():
    g.user_id = '1'
    auth_service = AuthService('secret')
    match_service = MatchService()

    # Check user 1 and user 3 are currently not matched
    matches_for_1 = match_service.get_current_matches()
    assert '3' not in matches_for_1.keys()
    g.user_id = '3'
    matches_for_3 = match_service.get_current_matches()
    assert '1' not in matches_for_3.keys()
    g.user_id = '1'

    # Check that only one match is generated because user 2 is
    # already in user 1's match history
    find_match_for_1 = match_service.find_match(1, 2)
    assert len(find_match_for_1) == 1

    # Check user 3 got added as an active match for user 1
    matches_for_1 = match_service.get_current_matches()
    assert len(matches_for_1) == 2
    assert matches_for_1['3']['profile']['interests'] == { '' : '' }

    # Check user 1 got added as an active match for user 3
    g.user_id = '3'
    matches_for_3 = match_service.get_current_matches()
    assert len(matches_for_3) == 1
    assert matches_for_3['1']['profile']['interests'] == { '' : '' }

