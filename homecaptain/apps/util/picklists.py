TITLEE_CHOICES = [
    ('', ''),
    ('Loan Officer', 'Loan Officer'),
    ('Team Lead', 'Team Lead'),
    ('Sales Manager', 'Sales Manager'),
    ('Purchasing', 'Purchasing'),
    ('Velocify Administrator', 'Velocify Administrator'),
    ('Vice President', 'Vice President'),
    ('Sales Assistant', 'Sales Assistant'),
    ('Production Assistant', 'Production Assistant'),
    ('Sales Agent', 'Sales Agent'),
    ('Branch Manager', 'Branch Manager'),
    ('Director', 'Director'),
    ('Purchase Loan Specialist', 'Purchase Loan Specialist'),
    ('Assistant Sales Manager', 'Assistant Sales Manager')
]

LEADSOURCE_CHOICES = [
    ('', ''),
    ('Advertisement', 'Advertisement'),
    ('Employee Referral', 'Employee Referral'),
    ('External Referral', 'External Referral'),
    ('Partner', 'Partner'),
    ('Public Relations', 'Public Relations'),
    ('Seminar - Partner', 'Seminar - Partner'),
    ('Trade Show', 'Trade Show'),
    ('Web', 'Web'),
    ('Word of mouth', 'Word of mouth'),
    ('Other', 'Other'),
    ('Great Plains', 'Great Plains'),
    ('NASB', 'NASB')
]

BUYER_SELLER_CHOICES = (
    ('', ''),
    ('Buyer', 'Buyer'),
    ('Seller', 'Seller'),
    ('Both', 'Both')
)
USER_TYPE_CHOICES = (
    ('Buyer', 'Buyer'),
    ('Seller', 'Seller'),
    ('Both', 'Both'),
    ('Realtor', 'Realtor'),
    ('Loan Officer', 'Loan Officer')
)

NON_HC_STAFF_USER_TYPES = ['Buyer', 'Seller', 'Both', 'Loan Officer', 'Realtor']

EVENT_CHOICES = [
    ('Property Showing', 'Property Showing'),
    ('Sign the Agent Document', 'Sign the Agent Document'),
]

RATING_CHOICES = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
]

# YES_NO_CHOICES = [
#   (True, 'Yes'),
#   (False, 'No'),
# ]

# YES_NO_NONE_CHOICES = [
#   (True, 'Yes'),
#   (False, 'No'),
#   (None, ''),
# ]

REALTOR_INTERESTS_CHOICES = [
    ('Becoming a Featured Agent?', 'Becoming a Featured Agent?'),
    ('Join our subscription list?', 'Join our subscription list?')
]

BUYER_MILESTONES_CHOICES = [
    ('Customer Still Searching for home', 'Still Searching for home'),
    ('Customer Offer Submitted', 'Offer Submitted'),
    ('Customer Ratified Contract', 'Ratified Contract'),
    ('Customer Closing Confirmed', 'Closing Confirmed'),
    ('Archived', 'Archived'),
    ('Searching Reset', 'Searching Reset'),
    ('Search for Home on Hold', 'Search on Hold'),
    ('Customer No Longer Looking', 'No Longer Looking'),
    ('Customer No Longer Responding', 'No Longer Responding'),
    ('Using a Different Realtor', 'Using a Different Realtor'),
    ('Unqualified', 'Unqualified')
]
#UI TEAM NEEDS THIS RESPONSE WHILE DJANGO NEEDS THE ABOVE
BUYER_MILESTONES_CHOICES_DICTS = [
    {
        'milestones': milestone[0],
        'milestones_display': milestone[1]
    } for milestone in BUYER_MILESTONES_CHOICES
]

SELLER_MILESTONES_CHOICES = [
    ('Archived', 'Archived'),
    ('Customer Closing Confirmed', 'Closing Confirmed'),
    ('Customer No Longer Responding', 'No Longer Responding'),
    ('Customer Ratified Contract', 'Ratified Contract'),
    ('Customer Home Listed', 'Home Listed'),
    ('Purchase Offer Submitted', 'Purchase Offer Submitted'),
    ('Home Sold', 'Home Sold')
]
#UI TEAM NEEDS THIS RESPONSE WHILE DJANGO NEEDS THE ABOVE
SELLER_MILESTONES_CHOICES_DICTS = [
    {
        'milestones': milestone[0],
        'milestones_display': milestone[1]
    } for milestone in SELLER_MILESTONES_CHOICES
]

MILESTONES_CHOICES = [
    ('Customer Still Searching for home', 'Still Searching for home'),
    ('Customer Offer Submitted', 'Offer Submitted'),
    ('Customer Ratified Contract', 'Ratified Contract'),
    ('Customer Closing Confirmed', 'Closing Confirmed'),
    ('Archived', 'Archived'),
    ('Searching Reset', 'Searching Reset'),
    ('Search for Home on Hold', 'Search on Hold'),
    ('Customer No Longer Looking', 'No Longer Looking'),
    ('Customer No Longer Responding', 'No Longer Responding'),
    ('Using a Different Realtor', 'Using a Different Realtor'),
    ('Unqualified', 'Unqualified'),
    ('Customer Home Listed', 'Home Listed'),
    ('Purchase Offer Submitted', 'Purchase Offer Submitted'),
    ('Home Sold', 'Home Sold')
]

MILESTONE_STATUS_REASON_CHOICES = [
    ('', ''),
    ('Considering Another Lender', 'Considering Another Lender'),
    ('Considering Another Realtor', 'Considering Another Realtor'),
    ('Realtor Not Responding', 'Realtor Not Responding'),
    ('Loan Officer Not Responding', 'Loan Officer Not Responding'),
    ('Found Another Realtor', 'Found Another Realtor'),
    ('Found Another Lender', 'Found Another Lender'),
    ('Customer Plans Fell Through', 'Customer Plans Fell Through'),
    ('Customer is No Longer Interested in Buying/Selling',
     'Customer is No Longer Interested in Buying/Selling'),
    ('Appointment Set', 'Appointment Set'),
    ('Viewing Homes', 'Viewing Homes')
]

ACCOUNT_TYPE_CHOICES = [
    ('', ''),
    ('Analyst', 'Analyst'),
    ('Competitor', 'Competitor'),
    ('Customer', 'Customer'),
    ('Integrator', 'Integrator'),
    ('Investor', 'Investor'),
    ('Partner', 'Partner'),
    ('Press', 'Press'),
    ('Prospect', 'Prospect'),
    ('Reseller', 'Reseller'),
    ('Other', 'Other')
]

TASK_DROPDOWN_CHOICES = [
    ('', ''),
    ('Agent Milestone Followup', 'Agent Milestone Followup'),
    ('Lead Follow up', 'Lead Follow up'),
    ('Lender Follow up', 'Lender Follow up')
]

# INDUSTRY_CHOICES = [
#     ('Agriculture', 'Agriculture'),
#     ('Apparel', 'Apparel'),
#     ('Banking', 'Banking'),
#     ('Biotechnology', 'Biotechnology'),
#     ('Chemicals', 'Chemicals'),
#     ('Communications', 'Communications'),
#     ('Construction', 'Construction'),
#     ('Consulting', 'Consulting'),
#     ('Education', 'Education'),
#     ('Electronics', 'Electronics'),
#     ('Energy', 'Energy'),
#     ('Engineering', 'Engineering'),
#     ('Entertainment', 'Entertainment'),
#     ('Environmental', 'Environmental'),
#     ('Finance', 'Finance'),
#     ('Food & Beverage', 'Food & Beverage'),
#     ('Government', 'Government'),
#     ('Healthcare', 'Healthcare'),
#     ('Hospitality', 'Hospitality'),
#     ('Insurance', 'Insurance'),
#     ('Machinery', 'Machinery'),
#     ('Manufacturing', 'Manufacturing'),
#     ('Media', 'Media'),
#     ('Not For Profit', 'Not For Profit'),
#     ('Other', 'Other'),
#     ('Recreation', 'Recreation'),
#     ('Retail', 'Retail'),
#     ('Shipping', 'Shipping'),
#     ('Technology', 'Technology'),
#     ('Telecommunications', 'Telecommunications'),
#     ('Transportation', 'Transportation'),
#     ('Utilities', 'Utilities')
# ]

# ACCOUNT_SOURCE_CHOICES = [
#     ('Advertisement', 'Advertisement'),
#     ('Employee Referral', 'Employee Referral'),
#     ('External Referral', 'External Referral'),
#     ('Partner', 'Partner'),
#     ('Public Relations', 'Public Relations'),
#     ('Seminar - Partner', 'Seminar - Partner'),
#     ('Trade Show', 'Trade Show'),
#     ('Web', 'Web'),
#     ('Word of mouth', 'Word of mouth'),
#     ('Other', 'Other'),
#     ('Great Plains', 'Great Plains'),
#     ('NASB', 'NASB')
# ]



##MLS STUFF
PROPERTY_TYPE_CHOICES = (
    ('Residential', 'Residential'),
    ('MultiFamily', 'MultiFamily')
)
ALLOWED_PROPERTY_TYPES = [e[0] for e in PROPERTY_TYPE_CHOICES]

PROPERTY_SUB_TYPE_CHOICES = (
    ('Cabin', 'Cabin'),
    ('Condominium', 'Condominium'),
    ('Duplex', 'Duplex'),
    ('Farm', 'Farm'),
    ('Manufactured Home', 'Manufactured Home'),
    ('Mobile Home', 'Mobile Home'),
    ('Quadruplex', 'Quadruplex'),
    ('Single Family Attached', 'Single Family Attached'),
    ('Single Family Detached', 'Single Family Detached'),
    ('Townhouse', 'Townhouse'),
    ('Triplex', 'Triplex')
)
ALLOWED_PROPERTY_SUB_TYPES = [e[0] for e in PROPERTY_SUB_TYPE_CHOICES]
