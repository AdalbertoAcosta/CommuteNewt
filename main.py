#!/usr/bin/python3

"""
Adalberto Acosta - 9/6/23
This is the main file, it's purpose is to scrape traffic information from Google Maps
and give an optimal time of departure via text message.
"""

from googleMapScraper import scrape_maps  # Scraper for Google Maps
from sms import send_mms_via_email  # Module to send text Messages


def main():
    address = "xyz home"  # Your address as it appears on Google Maps
    destination = "Seattle Pacific University"  # Your work or school

    driving = 1
    transit = 2
    walking = 3
    cycling = 4


    depart_time = scrape_maps(address, destination, driving, 9, 00, "am")  # Get departure time from scraper

    number = "1234567789"  # Phone number to receive departure time, no dashes and must be 10 digit
    message = depart_time  # Time to leave your home
    provider = "Cricket Wireless"  # Data service provider for your phone, must support sms or mms gateway

    file_path = "pngwing.com.png"  # Image that will be sent in mms text
    mime_maintype = "image"  # Standardized mime maintype for mms image
    mime_subtype = "png"  # Standardized mime subtype for mms image that is a png

    send_mms_via_email(number, message, file_path, mime_maintype, mime_subtype, provider, "Good Morning!")  # Send text message with arrival time


if __name__ == "__main__":
    main()
