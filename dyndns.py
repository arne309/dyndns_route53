import getip_ec2
import socket

hosts = ['server.r9y.de', 'unifi.r9y.de']
zoneId = "Z375FNAJJ0BS3F"

for host in hosts:
    print(host)

    try:
        dns_ipv4 = socket.getaddrinfo(host, None, socket.AF_INET)[0][4][0]
        dns_ipv6 = socket.getaddrinfo(host, None, socket.AF_INET6)[0][4][0]
    except socket.gaierror:
        print("Domain Name not found")
        dns_ipv4 = ""
        dns_ipv6 = ""

    my_ipv4 = getip_ec2.get_ipv4()
    my_ipv6 = getip_ec2.get_ipv6()

    if dns_ipv4!=my_ipv4 or dns_ipv6!=my_ipv6:
        print("Updating IP")
        import boto3
        client = boto3.client('route53')

        response = client.change_resource_record_sets(
            HostedZoneId=zoneId,
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': host,
                            'Type': 'A',
                            'TTL': 295,
                            'ResourceRecords': [{
                                    'Value': my_ipv4
                                }],
                        }
                    },
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': host,
                            'Type': 'AAAA',
                            'TTL': 295,
                            'ResourceRecords': [{
                                    'Value': my_ipv6
                                }],
                        }
                    }
                    ]
            }
        )

    else:
        print("IP is already up to date")

