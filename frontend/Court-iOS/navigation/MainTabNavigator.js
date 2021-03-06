import React from 'react';
import { Platform } from 'react-native';
import { createStackNavigator, createBottomTabNavigator } from 'react-navigation';

import Colors from '../constants/Colors';

import TabBarIcon from '../components/TabBarIcon';
import InboxScreen from '../screens/InboxScreen';
import ChatScreen from '../screens/ChatScreen';
import ChatProfileScreen from '../screens/ChatProfileScreen';
import LinksScreen from '../screens/LinksScreen';
import ProfileScreen from '../screens/ProfileScreen';

const HomeStack = createStackNavigator({
  Home: InboxScreen,
  Chats: ChatScreen,
  ChatProfile: ChatProfileScreen,
});

HomeStack.navigationOptions = {
  tabBarOptions: {
    activeTintColor: Colors.teal,
    labelStyle: {
      fontFamily: 'orkney-bold',
    },
  },
  tabBarLabel: 'Chats',
  tabBarIcon: ({ focused }) => (
    <TabBarIcon
      focused={focused}
      name='md-chatbubbles'
    />
  ),
};

const ProfileStack = createStackNavigator({
  Profile: ProfileScreen,
});

ProfileStack.navigationOptions = {
  tabBarOptions: {
    activeTintColor: Colors.teal,
    labelStyle: {
      fontFamily: 'orkney-bold',
    },
  },
  tabBarLabel: 'Profile',
  tabBarIcon: ({ focused }) => (
    <TabBarIcon
      focused={focused}
      name='md-person'
    />
  ),
};

export default createBottomTabNavigator({
  HomeStack,
  ProfileStack,
});
