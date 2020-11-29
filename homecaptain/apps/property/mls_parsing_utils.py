import dateutil
import json
import traceback

from bs4 import BeautifulSoup
from lxml import etree

from apps.util.picklists import ALLOWED_PROPERTY_TYPES, ALLOWED_PROPERTY_SUB_TYPES


def parse_feed_element(element):

    def get_node_text(scope, attribute_name):
        try:
            return scope.find(attribute_name).text
        except AttributeError:
            return ''
        
    def get_list_items(l, p, c):
        nl = []
        for e in l.find(p).findAll(c):
            if getattr(e, 'text', ''):
                nl.append(getattr(e, 'text'))
        return nl

    def to_int(value):
        try:
            return int(value)
        except ValueError:
            return 0
    
    element_string = etree.tostring(element, encoding='unicode', with_tail=False)
    soup = BeautifulSoup(element_string, features="lxml").find('listing')
    
    property_type = get_node_text(soup, 'propertytype')
    property_sub_type = get_node_text(soup, 'propertysubtype')

    if (property_type not in ALLOWED_PROPERTY_TYPES) or (property_sub_type not in ALLOWED_PROPERTY_SUB_TYPES):
        return
    
    listing = {
        'property_type': property_type,
        'property_sub_type': property_sub_type,
        'listing_key': get_node_text(soup, 'listingkey'),

        'target_price_maximum': to_int(get_node_text(soup, 'listprice')),
        'target_price_minimum': to_int(get_node_text(soup, 'listpricelow')),
        'listing_url': get_node_text(soup,'listingurl'),
        'bedrooms': to_int(get_node_text(soup, 'bedrooms')),
        'bathrooms': to_int(get_node_text(soup, 'bathrooms')),
        'square_feet': to_int(get_node_text(soup, 'livingarea')),
        'year_built': to_int(get_node_text(soup, 'yearbuilt')),
        'full_bathrooms': to_int(get_node_text(soup, 'fullbathrooms')),
        'three_quarter_bathrooms': to_int(get_node_text(soup, 'threequarterbathrooms')),
        'half_bathrooms': to_int(get_node_text(soup, 'halfbathrooms')),
        'one_quarter_bathrooms': to_int(get_node_text(soup, 'onequarterbathrooms')),

        'lead_routing_email': get_node_text(soup, 'leadroutingemail'),

        'listing_category': get_node_text(soup, 'listingcategory'),
        'disclose_address': True if get_node_text(soup, 'discloseaddress') == 'true' else False,
        'listing_description': get_node_text(soup, 'listingdescription'),
        'mls_number': get_node_text(soup, 'mlsnumber'),
        'listing_date': get_node_text(soup, 'listingdate'),
        'listing_title': get_node_text(soup, 'listingtitle'),
        'foreclosure_status': get_node_text(soup, 'foreclosurestatus'),
        'modification_timestamp': dateutil.parser.parse(soup.find('modificationtimestamp').text)
    }

    try:
        listing['lot_size'] = float(get_node_text(soup, 'lotsize'))
    except ValueError:
        pass

    try:
        address_soup = soup.find('address')
        listing['address'] = {
            'street': get_node_text(address_soup, 'commons:fullstreetaddress'),
            'unit_number': get_node_text(address_soup, 'commons:unitnumber'),
            'city': get_node_text(address_soup, 'commons:city'),
            'state': get_node_text(address_soup, 'commons:stateorprovince'),
            'postalcode': get_node_text(address_soup, 'commons:postalcode'),
        }
    except AttributeError:
        pass
    
    try:
        photos = soup.find('photos')
        listing.update({
            'photos': [
                {
                    'media_modification_timestamp': get_node_text(photo, 'mediamodificationtimestamp'),
                    'media_url': get_node_text(photo, 'mediaurl'),
                    'media_caption': get_node_text(photo, 'mediacaption'),
                    'media_description': get_node_text(photo, 'mediadescription')
                }
                for photo in photos.findAll('photo')
            ]
        })
    except AttributeError:
        pass
    

    try:
        listing_participants = soup.find('listingparticipants')
        listing.update({
            'listing_participants': [
                {
                    'first_name': get_node_text(participant, 'firstname'),
                    'last_name': get_node_text(participant, 'lastname'),
                    'role': get_node_text(participant, 'role'),
                    'office_phone': get_node_text(participant, 'officephone'),
                }
                for participant in listing_participants.findAll('participant')
            ]
        })
    except AttributeError:
        pass
    
    try:
        brokerage = soup.find('brokerage')
        listing.update({
            'brokerage': {
                'name': get_node_text(brokerage, 'name'),
            }
        })
    except AttributeError:
        pass
    
    try:
        location = soup.find('location')
        listing.update({
            'location': {
                'latitude': get_node_text(location, 'latitude'),
                'longitude': get_node_text(location, 'longitude'),
                'directions': get_node_text(location, 'directions'),
                'geocodeoptions': get_node_text(location, 'geocodeoptions'),
                'county': get_node_text(location, 'county'),
                'parcel_id': get_node_text(location, 'parcelid')
            }
        })
        
        try:
            community = location.find('community')
            listing['location'].update({
                'community': {
                    'subdivision': get_node_text(community, 'commons:subdivision'),
                    'schools': [
                        {
                            'name': get_node_text(school, 'commons:name'),
                            'school_category': get_node_text(school, 'commons:schoolcategory'),
                            'district': get_node_text(school, 'commons:district'),
                            'description': get_node_text(school, 'commons:description'),
                        }
                        for school in community.find('commons:schools').findAll('commons:school')
                    ]
                }
            })
        except AttributeError:
            pass
        
        
        try:
            neighborhoods = location.find('neighborhoods')
            listing['location'].update({
                'neighborhoods': [
                    {
                        'name': get_node_text(neighborhood, 'name'),
                        'description': get_node_text(neighborhood, 'description'),
                    }
                    for neighborhood in neighborhoods.findAll('neighborhood')
                ]
            })
        except AttributeError:
            pass
        
    except AttributeError:
        pass
    
    try:
        open_houses = soup.find('openhouses')
        listing.update({
            'open_houses': [
                {
                    'date': get_node_text(open_house, 'date'),
                    'start_time': get_node_text(open_house, 'starttime'),
                    'end_time': get_node_text(open_house, 'endtime'),
                    'description': get_node_text(open_house, 'description')
                }
                for open_house in open_houses.findAll('openhouse')
            ]
        })
    except AttributeError:
        pass
    
    
    try:
        taxes = soup.find('taxes')
        listing.update({
            'taxes': [
                {
                    'year': get_node_text(tax, 'year'),
                    'amount': get_node_text(tax, 'amount'),
                    'tax_description': get_node_text(tax, 'taxdescription')
                }
                for tax in taxes.findAll('tax')
            ]
        })
    except AttributeError:
        pass
    
    try:
        expenses = soup.find('expenses')
        listing['expenses'] = []
        for expense in expenses.findAll('expense'):
            category_name = get_node_text(expense, 'commons:expensecategory')
            if category_name not in ['Trash Fee', 'Yard Care Fee']:
                listing['expenses'].append({
                    'expense_category': category_name,
                    'expense_value': get_node_text(expense, 'commons:expensevalue'),
                })
    except AttributeError:
        pass
    
    
    try:
        detailed_characteristics = soup.find('detailedcharacteristics')
        listing.update({
            'detailed_characteristics': {
                'appliances': get_list_items(detailed_characteristics, 'appliances', 'appliance'),
                'has_attic': get_node_text(detailed_characteristics, 'hasattic'),
                'has_basement': get_node_text(detailed_characteristics, 'hasbasement'),
                'cooling_systems': get_list_items(detailed_characteristics, 'appliances', 'appliance'),
                'has_deck': get_node_text(detailed_characteristics, 'hasdeck'),
                'has_disabled_access': get_node_text(detailed_characteristics, 'hasdisabledaccess'),
                'has_dock': get_node_text(detailed_characteristics, 'hasdock'),
                'exterior_types': get_list_items(detailed_characteristics, 'appliances', 'appliance'),
                'has_fireplace': get_node_text(detailed_characteristics, 'hasfireplace'),
                'floor_coverings': get_list_items(detailed_characteristics, 'floorcoverings', 'floorcovering'),
                'has_gated_entry': get_node_text(detailed_characteristics, 'hasgatedentry'),
                'heating_systems': get_list_items(detailed_characteristics, 'heatingsystems', 'heatingsystem'),
                'legal_description': get_node_text(detailed_characteristics, 'legaldescription'),
                'num_floors': get_node_text(detailed_characteristics, 'numfloors'),
                'has_patio': get_node_text(detailed_characteristics, 'haspatio'),
                'has_pond': get_node_text(detailed_characteristics, 'haspond'),
                'has_pool': get_node_text(detailed_characteristics, 'haspool'),
                'has_porch': get_node_text(detailed_characteristics, 'hasporch'),
                'roof_types': get_list_items(detailed_characteristics, 'rooftypes', 'rooftype'),
                'view_types': get_list_items(detailed_characteristics, 'viewtypes', 'viewtype'),
                'is_waterfront': get_node_text(detailed_characteristics, 'iswaterfront'),
                'is_wired': get_node_text(detailed_characteristics, 'iswired'),
                'year_updated': get_node_text(detailed_characteristics, 'yearupdated'),
            }
        })
    except AttributeError:
        pass

    
    return listing
