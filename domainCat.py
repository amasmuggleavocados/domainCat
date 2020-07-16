#! /usr/bin/python3

from argparse import ArgumentParser
import argparse
import sys
from modules import *
import urllib
import re

parser = ArgumentParser(description='Domain Categorization Checking')
parser.add_argument('--domain', '-d', required=False, help='Domain name to lookup')
parser.add_argument('--service', '-s', nargs='?', const='a', help='Service to check Categorization against (Defaults to ALL) (a (ALL), b (Bluecoat), f (Fortiguard), i (IBM xForce), m (McAfee TrustedForce), w (WebSense), g (Google SafeBrowsing), p (PhishTank), c (Cisco Talos))')
parser.add_argument('--domain-list', '-l', required=False, help='List of domains')
parser.add_argument('--quiet', '-q', required=False, action='store_true', help='Suppress domainCat logo')
parser.add_argument('--expired_domain', '-e', required=False, action='store_true', help='Check category on top domains on expireddomains.net (use with -f)')
parser.add_argument('--filters', '-f', required=False, help='Domain Keyword to search on expireddomains.net')
parser.add_argument('--set_cat', required=False, action='store_true', help='Show how to set categorization for each service.')

class domainCat:

    def run(self, domain, service):
        if service == 'b':
            self.bluecoatCheck(domain)
        elif service == 'f':
            self.fortiguardCheck(domain)
        elif service == 'i':
            self.ibmCheck(domain)
        elif service == 'm':
            self.trustedsourceCheck(domain)
        elif service == 'w':
            self.websenseCheck(domain)
        elif service == 'g':
            self.googleCheck(domain)
        elif service == 'p':
            self.phishtankCheck(domain)
        #elif service == 'c':
            #self.ciscoCheck(domain)
        elif service == 'a':
            self.bluecoatCheck(domain)
            self.fortiguardCheck(domain)
            self.ibmCheck(domain)
            self.trustedsourceCheck(domain)
            self.websenseCheck(domain)
            #self.googleCheck(domain)
            #self.phishtankCheck(domain)
            #self.ciscoCheck(domain)

    def trustedsourceCheck(self, domain):
        print("\033[1;34m[*] Targeting McAfee Trustedsource\033[0;0m")
        ts = trustedsource.TrustedSource()
        ts.check_category(domain)

    def bluecoatCheck(self, domain):
        print("\033[1;34m[*] Targeting Bluecoat WebPulse\033[0;0m")
        b = bluecoat.Bluecoat()
        b.check_category(domain)

    def ibmCheck(self, domain):
        print("\033[1;34m[*] Targeting IBM Xforce\033[0;0m")
        xf = ibmxforce.IBMXforce()
        xf.checkIBMxForce(domain)

    def fortiguardCheck(self, domain):
        print("\033[1;34m[*] Targeting Fortiguard\033[0;0m")
        xf = fortiguard.Fortiguard()
        xf.check_category(domain)

    def websenseCheck(self, domain):            
        print("\033[1;34m[*] Targeting Websense\033[0;0m")
        xf = websense.Websense()
        xf.check_category(domain)

    def googleCheck(self, domain):
        print("Coming Soon")

    def phishtankCheck(self, domain):
        print("Coming Soon")

    def ciscoCheck(self, domain):
        print("\033[1;34m[*] Targeting Cisco Talos\033[0;0m")
        xf = ciscotalos.CiscoTalos()
        xf.check_category(domain)
        
    def expired_search(self, filename, argfilter):
        es = expireddomfilter.ExpiredDom()
        es.check_filter(filename, argfilter)
        
    def set_cat(self):
        sc = setcat.SetCategories()
        sc.set_cat()

    def asciiArt(self):
        print("""
   _
  ( \                ..-----..__
   \.'.        _.--'`  [   '  ' ```'-._
    `. `'-..-'' `    '  ' '   .  ;   ; `-'''-.,__/|/_
      `'-.;..-''`|'  `.  '.    ;     '  `    '   `'  `,
                 \ '   .    ' .     '   ;   .`   . ' 7 \\
                  '.' . '- . \    .`   .`  .   .\     `Y
                    '-.' .   ].  '   ,    '    /'`""';:'
                      /Y   '.] '-._ /    ' _.-'
                      \\'\_   ; (`'.'.'  ."/
                       ' )` /  `.'   .-'.'
                        '\  \).'  .-'--"
                          `. `,_'`
                            `.__)  
     domainCat - Domain Categorization Discovery at it's finest
     written by: l0gan""")

if __name__ == "__main__":
    dc = domainCat()
    args = parser.parse_args()

    quiet = args.quiet
    if not quiet:
        domainCat().asciiArt()
        
        
    if args.set_cat:
        dc.set_cat()
        exit()
    
    if args.expired_domain:
        if not args.filters:
            print('[-] Missing -f option')
        else:
            filename = args.filters + '.txt'
            dList = filename
            dc.expired_search(filename, args.filters)
    else:
        dList = args.domain_list
    
    service = args.service
    if not service:
        service = 'a'
    
    if not dList:
        domain = args.domain
        dc.run(domain, service)
    else:
        f = open(dList, 'r')
        for domain in f:
            dc.run(domain, service)
