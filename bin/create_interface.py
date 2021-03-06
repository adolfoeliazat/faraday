#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Faraday Penetration Test IDE
Copyright (C) 2016  Infobyte LLC (http://www.infobytesec.com/)
See the file 'doc/LICENSE' for the license information
"""

from model.common import factory
from persistence.server import models

__description__ = 'Creates a new interface in a specified host'
__prettyname__ = 'Create Interface'


def main(workspace='', args=None, parser=None):
    parser.add_argument('host_id', help='Host ID')
    parser.add_argument('name', help='Interface Name')
    parser.add_argument('mac', help='Interface MAC Address')

    parser.add_argument('--ipv4address', help='IPV4 Address', default='0.0.0.0')
    parser.add_argument('--ipv4gateway', help='IPV4 Gateway', default='0.0.0.0')
    parser.add_argument('--ipv4mask', help='IPV4 Mask', default='0.0.0.0')
    parser.add_argument('--ipv4dns', help='IPV4 DNS, as a comma separated list', default='')

    parser.add_argument('--ipv6address', help='IPV6 Address', default='0000:0000:0000:0000:0000:0000:0000:0000')
    parser.add_argument('--ipv6prefix', help='IPV6 Prefix', default='00')
    parser.add_argument('--ipv6gateway', help='IPV4 Gateway', default='0000:0000:0000:0000:0000:0000:0000:0000')
    parser.add_argument('--ipv6dns', help='IPV6 DNS, as a comma separated list', default='')

    parser.add_argument('--netsegment', help='Network Segment', default='')
    parser.add_argument('--hostres', help='Hostname Resolution', default='')

    parser.add_argument('--dry-run', action='store_true', help='Do not touch the database. Only print the object ID')

    parsed_args = parser.parse_args(args)

    ipv4_dns = filter(None, parsed_args.ipv4dns.split(','))
    ipv6_dns = filter(None, parsed_args.ipv6dns.split(','))

    obj = factory.createModelObject(models.Interface.class_signature, parsed_args.name, workspace,
                                    mac=parsed_args.mac,
                                    ipv4_address=parsed_args.ipv4address,
                                    ipv4_mask=parsed_args.ipv4mask,
                                    ipv4_gateway=parsed_args.ipv4gateway,
                                    ipv4_dns=ipv4_dns,
                                    ipv6_address=parsed_args.ipv6address,
                                    ipv6_prefix=parsed_args.ipv6prefix,
                                    ipv6_gateway=parsed_args.ipv6gateway,
                                    ipv6_dns=ipv6_dns,
                                    network_segment=parsed_args.netsegment,
                                    hostname_resolution=parsed_args.hostres,
                                    parent_id=parsed_args.host_id)

    old = models.get_interface(workspace, obj.getID())

    if old is None:
        if not parsed_args.dry_run:
            models.create_interface(workspace, obj)
    else:
        print "An interface with ID %s already exists!" % obj.getID()
        return 2, None

    return 0, obj.getID()
