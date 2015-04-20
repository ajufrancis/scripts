#!/usr/bin/python
#coding:utf-8
import sys, os
import requests
import pprint

def make_request(endpoint, api_key, secret_key, payload={}):
    payload['response'] = 'json'
    payload['apikey'] = api_key
