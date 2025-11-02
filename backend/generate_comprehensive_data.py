"""
Generate comprehensive datasets with GENUINE entries for ALL quiz options
Matches exactly what users see in the onboarding quiz
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# ==================== MUSIC DATA ====================
print("🎵 Generating comprehensive music data...")

music_genres_quiz = ['Pop', 'Rock', 'Hip Hop', 'Jazz', 'Classical', 'Electronic', 'Country', 'R&B', 'Indie', 'Metal']

# Expanded artist database with REAL songs by genre
music_data = {
    'Pop': {
        'Taylor Swift': ['Shake It Off', 'Blank Space', 'Love Story', 'You Belong With Me', 'Anti-Hero', 'Cruel Summer', 'Cardigan', 'Willow', 'Bad Blood', 'Style', '22', 'We Are Never Getting Back Together'],
        'Ariana Grande': ['Thank U Next', '7 Rings', 'Problem', 'Side To Side', 'Break Free', 'God Is A Woman', 'Positions', 'Into You', 'Dangerous Woman', 'No Tears Left To Cry'],
        'Ed Sheeran': ['Shape of You', 'Perfect', 'Thinking Out Loud', 'Photograph', 'Castle on the Hill', 'Galway Girl', 'Bad Habits', 'Shivers', 'Happier', 'Lego House'],
        'Dua Lipa': ['Levitating', 'Don\'t Start Now', 'New Rules', 'One Kiss', 'Physical', 'Break My Heart', 'IDGAF', 'Be The One', 'Hotter Than Hell', 'Blow Your Mind'],
        'The Weeknd': ['Blinding Lights', 'Starboy', 'The Hills', 'Can\'t Feel My Face', 'Save Your Tears', 'I Feel It Coming', 'Heartless', 'Die For You', 'Earned It', 'Call Out My Name'],
    },
    'Rock': {
        'Queen': ['Bohemian Rhapsody', 'We Will Rock You', 'We Are The Champions', 'Don\'t Stop Me Now', 'Another One Bites The Dust', 'Somebody To Love', 'Under Pressure', 'Radio Ga Ga', 'I Want To Break Free', 'Killer Queen'],
        'The Beatles': ['Hey Jude', 'Let It Be', 'Yesterday', 'Come Together', 'Here Comes The Sun', 'A Hard Day\'s Night', 'Help!', 'All You Need Is Love', 'Twist And Shout', 'Get Back'],
        'Led Zeppelin': ['Stairway to Heaven', 'Whole Lotta Love', 'Kashmir', 'Black Dog', 'Rock and Roll', 'Immigrant Song', 'Ramble On', 'Good Times Bad Times', 'Dazed and Confused', 'When the Levee Breaks'],
        'Imagine Dragons': ['Radioactive', 'Demons', 'Believer', 'Thunder', 'Whatever It Takes', 'It\'s Time', 'On Top Of The World', 'Natural', 'Bad Liar', 'Warriors'],
        'Coldplay': ['Yellow', 'Fix You', 'Viva La Vida', 'The Scientist', 'Clocks', 'Paradise', 'A Sky Full Of Stars', 'Adventure Of A Lifetime', 'Hymn For The Weekend', 'Speed Of Sound'],
    },
    'Hip Hop': {
        'Drake': ['God\'s Plan', 'One Dance', 'Hotline Bling', 'In My Feelings', 'Nice For What', 'Started From The Bottom', 'Take Care', 'Hold On We\'re Going Home', 'Passionfruit', 'Controlla'],
        'Kendrick Lamar': ['HUMBLE.', 'DNA.', 'Swimming Pools', 'Alright', 'King Kunta', 'm.A.A.d city', 'Money Trees', 'Bitch Don\'t Kill My Vibe', 'Poetic Justice', 'The Blacker The Berry'],
        'Eminem': ['Lose Yourself', 'Without Me', 'Stan', 'The Real Slim Shady', 'Not Afraid', 'Love The Way You Lie', 'Mockingbird', 'Till I Collapse', 'Rap God', 'Cleanin\' Out My Closet'],
        'Post Malone': ['Circles', 'Sunflower', 'Rockstar', 'Congratulations', 'Better Now', 'Psycho', 'White Iverson', 'I Fall Apart', 'Wow', 'Goodbyes'],
        'Travis Scott': ['SICKO MODE', 'Goosebumps', 'Antidote', 'Highest In The Room', 'Butterfly Effect', 'Stargazing', '90210', '3500', 'Pick Up The Phone', 'Wake Up'],
    },
    'R&B': {
        'Rihanna': ['Umbrella', 'Diamonds', 'We Found Love', 'Work', 'Stay', 'Love On The Brain', 'Only Girl', 'What\'s My Name', 'Don\'t Stop The Music', 'Disturbia'],
        'The Weeknd': ['Earned It', 'Die For You', 'Call Out My Name', 'Often', 'The Morning', 'Wicked Games', 'High For This', 'Crew Love', 'Acquainted', 'In The Night'],
        'Beyoncé': ['Crazy In Love', 'Single Ladies', 'Halo', 'Irreplaceable', 'Formation', 'Drunk In Love', 'Love On Top', 'Run The World', 'If I Were A Boy', 'Partition'],
        'Frank Ocean': ['Thinkin Bout You', 'Pyramids', 'Novacane', 'Swim Good', 'Pink + White', 'Nikes', 'Self Control', 'Ivy', 'Nights', 'Lost'],
        'SZA': ['The Weekend', 'Good Days', 'Love Galore', 'All The Stars', 'Broken Clocks', 'Drew Barrymore', 'Garden', 'Prom', 'Supermodel', 'Normal Girl'],
    },
    'Indie': {
        'Arctic Monkeys': ['Do I Wanna Know?', 'Why\'d You Only Call Me When You\'re High?', 'R U Mine?', 'I Bet You Look Good On The Dancefloor', 'Fluorescent Adolescent', '505', 'Arabella', 'Crying Lightning', 'Cornerstone', 'Tranquility Base Hotel'],
        'Tame Impala': ['The Less I Know The Better', 'Let It Happen', 'Feels Like We Only Go Backwards', 'Borderline', 'Elephant', 'Eventually', 'New Person Same Old Mistakes', 'Lost In Yesterday', 'The Moment', 'Mind Mischief'],
        'The Strokes': ['Reptilia', 'Last Nite', 'Someday', 'Under Cover Of Darkness', 'You Only Live Once', 'Juicebox', 'Hard To Explain', '12:51', 'The Modern Age', 'Barely Legal'],
        'Foster The People': ['Pumped Up Kicks', 'Sit Next To Me', 'Houdini', 'Helena Beat', 'Don\'t Stop', 'Coming Of Age', 'Best Friend', 'Waste', 'Broken Jaw', 'Call It What You Want'],
        'MGMT': ['Electric Feel', 'Kids', 'Time To Pretend', 'Little Dark Age', 'Congratulations', 'Me And Michael', 'When You Die', 'She Works Out Too Much', 'TSLAMP', 'Flash Delirium'],
    },
    'Electronic': {
        'Daft Punk': ['Get Lucky', 'One More Time', 'Harder Better Faster Stronger', 'Around The World', 'Something About Us', 'Digital Love', 'Technologic', 'Instant Crush', 'Lose Yourself To Dance', 'Da Funk'],
        'Calvin Harris': ['Summer', 'Feel So Close', 'This Is What You Came For', 'Acceptable In The 80s', 'Sweet Nothing', 'How Deep Is Your Love', 'Outside', 'Thinking About You', 'Blame', 'I Need Your Love'],
        'Avicii': ['Wake Me Up', 'Levels', 'Hey Brother', 'Waiting For Love', 'The Nights', 'Without You', 'You Make Me', 'Addicted To You', 'Seek Bromance', 'Silhouettes'],
        'Marshmello': ['Alone', 'Happier', 'Silence', 'Friends', 'Wolves', 'Here With Me', 'Ritual', 'Find Me', 'Leave Before You Love Me', 'OK Not To Be OK'],
        'Kygo': ['Firestone', 'Stole The Show', 'It Ain\'t Me', 'Higher Love', 'Happy Now', 'Stargazing', 'Stay', 'Forever Yours', 'Carry On', 'Remind Me To Forget'],
    },
    'Jazz': {
        'Miles Davis': ['So What', 'Blue In Green', 'All Blues', 'Freddie Freeloader', 'Flamenco Sketches', 'My Funny Valentine', 'Round Midnight', 'Summertime', 'Autumn Leaves', 'Bye Bye Blackbird'],
        'John Coltrane': ['A Love Supreme Part 1', 'Giant Steps', 'My Favorite Things', 'Blue Train', 'Naima', 'Impressions', 'Central Park West', 'Alabama', 'Equinox', 'Countdown'],
        'Billie Holiday': ['Strange Fruit', 'God Bless The Child', 'Summertime', 'Lover Man', 'Don\'t Explain', 'I\'ll Be Seeing You', 'What A Little Moonlight Can Do', 'Easy Living', 'Solitude', 'The Man I Love'],
        'Ella Fitzgerald': ['Dream A Little Dream', 'Summertime', 'It Don\'t Mean A Thing', 'A-Tisket A-Tasket', 'Someone To Watch Over Me', 'Cry Me A River', 'Cheek To Cheek', 'How High The Moon', 'Mack The Knife', 'Blue Skies'],
        'Louis Armstrong': ['What A Wonderful World', 'Hello Dolly', 'La Vie En Rose', 'When The Saints Go Marching In', 'Dream A Little Dream', 'Blueberry Hill', 'A Kiss To Build A Dream On', 'Stardust', 'Mack The Knife', 'West End Blues'],
    },
    'Classical': {
        'Ludwig van Beethoven': ['Symphony No. 9', 'Für Elise', 'Moonlight Sonata', 'Symphony No. 5', 'Ode To Joy', 'Piano Concerto No. 5', 'Pathétique Sonata', 'Appassionata', 'Violin Concerto', 'Symphony No. 7'],
        'Wolfgang Amadeus Mozart': ['Eine kleine Nachtmusik', 'Requiem', 'Symphony No. 40', 'Piano Concerto No. 21', 'The Magic Flute Overture', 'Don Giovanni', 'Turkish March', 'Clarinet Concerto', 'Jupiter Symphony', 'Ave Verum Corpus'],
        'Johann Sebastian Bach': ['Toccata and Fugue in D minor', 'Air on the G String', 'Brandenburg Concerto No. 3', 'Cello Suite No. 1', 'Goldberg Variations', 'The Well-Tempered Clavier', 'Mass in B minor', 'Jesu Joy', 'Prelude in C Major', 'Chaconne'],
        'Frédéric Chopin': ['Nocturne Op. 9 No. 2', 'Waltz in A minor', 'Fantaisie-Impromptu', 'Ballade No. 1', 'Étude Op. 10 No. 3', 'Polonaise Op. 53', 'Prelude in E minor', 'Waltz in C# minor', 'Nocturne in E-flat', 'Mazurka Op. 68'],
        'Pyotr Tchaikovsky': ['Swan Lake', 'The Nutcracker Suite', '1812 Overture', 'Dance of the Sugar Plum Fairy', 'Sleeping Beauty Waltz', 'Romeo and Juliet Overture', 'Piano Concerto No. 1', 'Symphony No. 6', 'Waltz of the Flowers', 'March from Nutcracker'],
    },
    'Country': {
        'Johnny Cash': ['Ring of Fire', 'I Walk The Line', 'Folsom Prison Blues', 'Hurt', 'A Boy Named Sue', 'Man In Black', 'Jackson', 'Get Rhythm', 'Sunday Morning Coming Down', 'One'],
        'Dolly Parton': ['Jolene', '9 to 5', 'I Will Always Love You', 'Coat of Many Colors', 'Here You Come Again', 'Islands In The Stream', 'Two Doors Down', 'Why\'d You Come In Here', 'Eagle When She Flies', 'Rockin\' Years'],
        'Carrie Underwood': ['Before He Cheats', 'Jesus Take The Wheel', 'Blown Away', 'Something In The Water', 'Cowboy Casanova', 'Good Girl', 'Undo It', 'Last Name', 'Two Black Cadillacs', 'Church Bells'],
        'Luke Bryan': ['Country Girl', 'Drunk On You', 'Play It Again', 'That\'s My Kind Of Night', 'Crash My Party', 'Strip It Down', 'Knockin\' Boots', 'I Don\'t Want This Night To End', 'Do I', 'Most People Are Good'],
        'Taylor Swift': ['Tim McGraw', 'Teardrops On My Guitar', 'Our Song', 'Picture To Burn', 'Should\'ve Said No', 'Love Story', 'You Belong With Me', 'Fifteen', 'Fearless', 'White Horse'],
    },
    'Metal': {
        'Metallica': ['Enter Sandman', 'Master of Puppets', 'Nothing Else Matters', 'One', 'Fade To Black', 'For Whom The Bell Tolls', 'Seek & Destroy', 'Battery', 'Ride The Lightning', 'The Unforgiven'],
        'Iron Maiden': ['The Trooper', 'Fear Of The Dark', 'Run To The Hills', 'Hallowed Be Thy Name', 'Number Of The Beast', 'Aces High', 'Wasted Years', 'Can I Play With Madness', 'Powerslave', '2 Minutes To Midnight'],
        'Black Sabbath': ['Paranoid', 'Iron Man', 'War Pigs', 'Heaven And Hell', 'N.I.B.', 'Sweet Leaf', 'Children Of The Grave', 'The Wizard', 'Planet Caravan', 'Sabbath Bloody Sabbath'],
        'Slayer': ['Raining Blood', 'Angel of Death', 'South of Heaven', 'Seasons In The Abyss', 'War Ensemble', 'Dead Skin Mask', 'Mandatory Suicide', 'Postmortem', 'Chemical Warfare', 'Hell Awaits'],
        'Slipknot': ['Psychosocial', 'Duality', 'Wait And Bleed', 'Before I Forget', 'The Devil In I', 'Snuff', 'Left Behind', 'Vermilion', 'Spit It Out', 'Eyeless'],
    }
}

# Create tracks dataset
tracks = []
track_id = 1

for genre, artists in music_data.items():
    for artist, songs in artists.items():
        for song in songs:
            duration = random.randint(180, 360)  # 3-6 minutes
            year = random.randint(1960, 2024)
            album = f"{artist} - Album {random.randint(1, 10)}"
            
            tracks.append({
                'track_id': track_id,
                'title': song,
                'artist': artist,
                'album': album,
                'genre': genre,
                'duration': duration,
                'year': year
            })
            track_id += 1

tracks_df = pd.DataFrame(tracks)
print(f"✓ Generated {len(tracks_df)} tracks across {len(music_genres_quiz)} genres")
print(f"  Genre distribution: {tracks_df['genre'].value_counts().to_dict()}")

# Generate listening history (30,000 interactions)
num_users = 100
num_listens = 30000

listening_history = []
for _ in range(num_listens):
    user_id = random.randint(1, num_users)
    track_id = random.randint(1, len(tracks_df))
    play_count = random.randint(1, 50)
    timestamp = datetime.now() - timedelta(days=random.randint(0, 365))
    
    listening_history.append({
        'user_id': user_id,
        'track_id': track_id,
        'play_count': play_count,
        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S')
    })

listening_df = pd.DataFrame(listening_history)
print(f"✓ Generated {len(listening_df)} listening history records")

# Save music data
tracks_df.to_csv('../data/tracks.csv', index=False)
listening_df.to_csv('../data/listening_history.csv', index=False)
print("✓ Music data saved!\n")

# ==================== MOVIE DATA - Already has good data from MovieLens ====================
print("🎬 Movie data already comprehensive (MovieLens 100K)")
print("   Skipping movie generation...\n")

# ==================== PRODUCT DATA ====================
print("🛍️ Generating comprehensive product data...")

shopping_categories_quiz = ['Electronics', 'Fashion', 'Books', 'Home & Garden', 'Sports', 
                            'Beauty', 'Toys', 'Food', 'Health', 'Automotive']

products_data = {
    'Electronics': [
        ('iPhone 15 Pro Max', 'Apple', 1199.99),
        ('Samsung Galaxy S24 Ultra', 'Samsung', 1299.99),
        ('MacBook Pro 16"', 'Apple', 2499.99),
        ('Dell XPS 15', 'Dell', 1899.99),
        ('Sony WH-1000XM5 Headphones', 'Sony', 399.99),
        ('AirPods Pro 2', 'Apple', 249.99),
        ('iPad Air', 'Apple', 599.99),
        ('Samsung Galaxy Tab S9', 'Samsung', 799.99),
        ('PlayStation 5', 'Sony', 499.99),
        ('Xbox Series X', 'Microsoft', 499.99),
        ('Nintendo Switch OLED', 'Nintendo', 349.99),
        ('LG OLED TV 65"', 'LG', 2199.99),
        ('Sony Bravia 4K TV', 'Sony', 1299.99),
        ('Canon EOS R6', 'Canon', 2499.99),
        ('GoPro Hero 12', 'GoPro', 399.99),
    ],
    'Fashion': [
        ('Nike Air Max 270', 'Nike', 150.00),
        ('Adidas Ultraboost', 'Adidas', 180.00),
        ('Levi\'s 501 Jeans', 'Levi\'s', 98.00),
        ('Ray-Ban Aviator Sunglasses', 'Ray-Ban', 153.00),
        ('Gucci Belt', 'Gucci', 450.00),
        ('North Face Jacket', 'The North Face', 299.00),
        ('Patagonia Fleece', 'Patagonia', 149.00),
        ('Timberland Boots', 'Timberland', 198.00),
        ('Vans Old Skool', 'Vans', 65.00),
        ('Converse Chuck Taylor', 'Converse', 60.00),
        ('Tommy Hilfiger Polo', 'Tommy Hilfiger', 79.00),
        ('Ralph Lauren Sweater', 'Ralph Lauren', 145.00),
        ('Carhartt Workwear', 'Carhartt', 89.00),
        ('Columbia Hiking Pants', 'Columbia', 75.00),
        ('Under Armour Sports Bra', 'Under Armour', 49.99),
    ],
    'Books': [
        ('Atomic Habits', 'James Clear', 16.99),
        ('The Psychology of Money', 'Morgan Housel', 14.99),
        ('Sapiens', 'Yuval Noah Harari', 17.99),
        ('Educated', 'Tara Westover', 15.99),
        ('Thinking Fast and Slow', 'Daniel Kahneman', 18.99),
        ('The Alchemist', 'Paulo Coelho', 14.99),
        ('1984', 'George Orwell', 13.99),
        ('To Kill a Mockingbird', 'Harper Lee', 12.99),
        ('Harry Potter Box Set', 'J.K. Rowling', 65.00),
        ('Lord of the Rings', 'J.R.R. Tolkien', 35.00),
        ('The Great Gatsby', 'F. Scott Fitzgerald', 10.99),
        ('Pride and Prejudice', 'Jane Austen', 9.99),
        ('The Subtle Art of Not Giving a F*ck', 'Mark Manson', 14.99),
        ('Becoming', 'Michelle Obama', 19.99),
        ('Can\'t Hurt Me', 'David Goggins', 16.99),
    ],
    'Home & Garden': [
        ('Dyson V15 Vacuum', 'Dyson', 649.99),
        ('Instant Pot Duo', 'Instant Pot', 99.99),
        ('KitchenAid Stand Mixer', 'KitchenAid', 379.99),
        ('Ninja Air Fryer', 'Ninja', 129.99),
        ('Keurig Coffee Maker', 'Keurig', 139.99),
        ('iRobot Roomba', 'iRobot', 599.99),
        ('Philips Hue Lights', 'Philips', 199.99),
        ('Nest Thermostat', 'Google', 129.99),
        ('Ring Video Doorbell', 'Ring', 99.99),
        ('Anova Sous Vide', 'Anova', 199.00),
        ('Le Creuset Dutch Oven', 'Le Creuset', 349.95),
        ('Vitamix Blender', 'Vitamix', 449.99),
        ('Shark Steam Mop', 'Shark', 99.99),
        ('Crock-Pot Slow Cooker', 'Crock-Pot', 49.99),
        ('Weber Grill', 'Weber', 499.00),
    ],
    'Sports': [
        ('Peloton Bike', 'Peloton', 1445.00),
        ('Bowflex Dumbbells', 'Bowflex', 549.00),
        ('Yeti Cooler 45', 'Yeti', 325.00),
        ('Hydro Flask Water Bottle', 'Hydro Flask', 44.95),
        ('Fitbit Charge 6', 'Fitbit', 159.95),
        ('Garmin Forerunner 945', 'Garmin', 599.99),
        ('Wilson Football', 'Wilson', 29.99),
        ('Spalding Basketball', 'Spalding', 49.99),
        ('Callaway Golf Clubs', 'Callaway', 1299.99),
        ('TaylorMade Driver', 'TaylorMade', 599.99),
        ('Trek Mountain Bike', 'Trek', 1899.00),
        ('Specialized Road Bike', 'Specialized', 2499.00),
        ('Bose Sport Earbuds', 'Bose', 179.00),
        ('Adidas Soccer Ball', 'Adidas', 39.99),
        ('Easton Baseball Bat', 'Easton', 299.99),
    ],
    'Beauty': [
        ('Dyson Airwrap', 'Dyson', 599.99),
        ('Fenty Beauty Foundation', 'Fenty', 39.00),
        ('MAC Lipstick', 'MAC', 19.00),
        ('Urban Decay Eyeshadow Palette', 'Urban Decay', 54.00),
        ('Clinique Moisturizer', 'Clinique', 38.50),
        ('The Ordinary Skincare Set', 'The Ordinary', 45.00),
        ('Glossier Boy Brow', 'Glossier', 18.00),
        ('Olaplex Hair Treatment', 'Olaplex', 28.00),
        ('Anastasia Beverly Hills Brow Kit', 'Anastasia', 29.00),
        ('Tatcha Water Cream', 'Tatcha', 68.00),
        ('Charlotte Tilbury Pillow Talk', 'Charlotte Tilbury', 34.00),
        ('La Mer Face Cream', 'La Mer', 345.00),
        ('Drunk Elephant Vitamin C', 'Drunk Elephant', 80.00),
        ('Bioderma Micellar Water', 'Bioderma', 14.99),
        ('CeraVe Daily Moisturizer', 'CeraVe', 16.99),
    ],
    'Toys': [
        ('LEGO Star Wars Millennium Falcon', 'LEGO', 169.99),
        ('LEGO Technic Bugatti', 'LEGO', 379.99),
        ('Barbie Dream House', 'Mattel', 199.99),
        ('Hot Wheels Track Set', 'Mattel', 49.99),
        ('Nerf N-Strike Elite', 'Nerf', 39.99),
        ('Play-Doh Super Set', 'Play-Doh', 24.99),
        ('Fisher-Price Baby Toys', 'Fisher-Price', 29.99),
        ('Monopoly Board Game', 'Hasbro', 19.99),
        ('Jenga Classic', 'Hasbro', 14.99),
        ('Uno Card Game', 'Mattel', 9.99),
        ('Rubik\'s Cube', 'Rubik\'s', 12.99),
        ('Melissa & Doug Puzzles', 'Melissa & Doug', 19.99),
        ('Disney Princess Doll', 'Disney', 24.99),
        ('Marvel Action Figures', 'Hasbro', 34.99),
        ('Nintendo Mario Kart RC', 'Nintendo', 79.99),
    ],
    'Food': [
        ('Starbucks Coffee Beans', 'Starbucks', 12.99),
        ('Nutella Hazelnut Spread', 'Nutella', 7.99),
        ('KIND Protein Bars', 'KIND', 18.99),
        ('Clif Energy Bars', 'Clif', 14.99),
        ('La Croix Sparkling Water', 'La Croix', 5.99),
        ('Ghirardelli Chocolate', 'Ghirardelli', 9.99),
        ('Blue Diamond Almonds', 'Blue Diamond', 6.99),
        ('Nature Valley Granola', 'Nature Valley', 8.99),
        ('Pringles Chips', 'Pringles', 2.99),
        ('Oreo Cookies', 'Oreo', 4.99),
        ('Ben & Jerry\'s Ice Cream', 'Ben & Jerry\'s', 5.99),
        ('Kellogg\'s Cereal', 'Kellogg\'s', 4.49),
        ('Annie\'s Mac & Cheese', 'Annie\'s', 3.99),
        ('Heinz Ketchup', 'Heinz', 3.49),
        ('Sriracha Hot Sauce', 'Huy Fong', 4.99),
    ],
    'Health': [
        ('Optimum Nutrition Whey Protein', 'Optimum Nutrition', 59.99),
        ('Nature Made Multivitamins', 'Nature Made', 24.99),
        ('Emergen-C Vitamin C', 'Emergen-C', 14.99),
        ('Braun Thermometer', 'Braun', 39.99),
        ('Omron Blood Pressure Monitor', 'Omron', 79.99),
        ('AccuChek Glucose Meter', 'AccuChek', 29.99),
        ('Advil Pain Relief', 'Advil', 12.99),
        ('Tylenol Extra Strength', 'Tylenol', 14.99),
        ('Claritin Allergy Relief', 'Claritin', 29.99),
        ('Zyrtec Antihistamine', 'Zyrtec', 24.99),
        ('Neosporin First Aid', 'Neosporin', 8.99),
        ('Band-Aid Bandages', 'Band-Aid', 6.99),
        ('Theragun Massage Gun', 'Theragun', 299.00),
        ('Withings Smart Scale', 'Withings', 99.95),
        ('Pure Enrichment Humidifier', 'Pure Enrichment', 49.99),
    ],
    'Automotive': [
        ('Michelin Tires Set', 'Michelin', 699.99),
        ('Bosch Wiper Blades', 'Bosch', 29.99),
        ('Garmin GPS Navigator', 'Garmin', 199.99),
        ('Armor All Car Wax', 'Armor All', 12.99),
        ('Meguiar\'s Car Polish', 'Meguiar\'s', 19.99),
        ('Chemical Guys Wash Kit', 'Chemical Guys', 49.99),
        ('WeatherTech Floor Mats', 'WeatherTech', 139.99),
        ('Thule Roof Rack', 'Thule', 399.99),
        ('Anker Car Charger', 'Anker', 24.99),
        ('Nextbase Dash Cam', 'Nextbase', 179.99),
        ('Optima Car Battery', 'Optima', 249.99),
        ('K&N Air Filter', 'K&N', 59.99),
        ('Rain-X Windshield Treatment', 'Rain-X', 7.99),
        ('Craftsman Tool Set', 'Craftsman', 199.99),
        ('Black+Decker Jump Starter', 'Black+Decker', 79.99),
    ]
}

products = []
product_id = 1

for category, items in products_data.items():
    for name, brand, price in items:
        rating = round(random.uniform(3.5, 5.0), 1)
        num_reviews = random.randint(100, 5000)
        in_stock = random.choice([True, True, True, False])  # 75% in stock
        
        products.append({
            'product_id': product_id,
            'title': name,  # Changed from 'name' to 'title' to match recommender expectations
            'brand': brand,
            'category': category,
            'price': price,
            'rating': rating,
            'num_reviews': num_reviews,
            'in_stock': in_stock
        })
        product_id += 1

products_df = pd.DataFrame(products)
print(f"✓ Generated {len(products_df)} products across {len(shopping_categories_quiz)} categories")
print(f"  Category distribution: {products_df['category'].value_counts().to_dict()}")

# Generate purchase history (40,000 reviews)
num_reviews = 40000
reviews = []

for _ in range(num_reviews):
    user_id = random.randint(1, num_users)
    product_id = random.randint(1, len(products_df))
    rating = random.randint(1, 5)
    timestamp = datetime.now() - timedelta(days=random.randint(0, 730))
    
    reviews.append({
        'user_id': user_id,
        'product_id': product_id,
        'rating': rating,
        'timestamp': timestamp.strftime('%Y-%m-%d')
    })

reviews_df = pd.DataFrame(reviews)
print(f"✓ Generated {len(reviews_df)} product reviews")

products_df.to_csv('../data/products.csv', index=False)
reviews_df.to_csv('../data/reviews.csv', index=False)
print("✓ Product data saved!\n")

# ==================== COURSE DATA ====================
print("📚 Generating comprehensive course data...")

learning_topics_quiz = ['Programming', 'Business', 'Design', 'Marketing', 'Data Science',
                        'Languages', 'Music', 'Photography', 'Finance', 'Health']

courses_data = {
    'Programming': [
        ('Complete Python Bootcamp', 'Jose Portilla', 'Beginner'),
        ('The Web Developer Bootcamp', 'Colt Steele', 'Beginner'),
        ('JavaScript: Understanding the Weird Parts', 'Anthony Alicea', 'Intermediate'),
        ('React - The Complete Guide', 'Maximilian Schwarzmüller', 'Intermediate'),
        ('Node.js The Complete Guide', 'Maximilian Schwarzmüller', 'Intermediate'),
        ('iOS App Development', 'Angela Yu', 'Beginner'),
        ('Android Java Masterclass', 'Tim Buchalka', 'Intermediate'),
        ('Complete C# Unity Game Developer', 'Ben Tristem', 'Beginner'),
        ('Machine Learning A-Z', 'Kirill Eremenko', 'Advanced'),
        ('Complete SQL Bootcamp', 'Jose Portilla', 'Beginner'),
        ('Docker Mastery', 'Bret Fisher', 'Intermediate'),
        ('AWS Certified Solutions Architect', 'Ryan Kroonenburg', 'Advanced'),
        ('Git Complete', 'Jason Taylor', 'Beginner'),
        ('Python for Data Science', 'Jose Portilla', 'Intermediate'),
        ('Full Stack Web Development', 'Rob Percival', 'Intermediate'),
    ],
    'Business': [
        ('An Entire MBA in 1 Course', 'Chris Haroun', 'Intermediate'),
        ('Business Strategy', 'Mike Figliuolo', 'Advanced'),
        ('Project Management Professional', 'Joseph Phillips', 'Intermediate'),
        ('The Complete Management Course', 'Chris Croft', 'Beginner'),
        ('Startup Launch Formula', 'Steve Blank', 'Intermediate'),
        ('Business Analytics', 'Kirill Eremenko', 'Intermediate'),
        ('Supply Chain Management', 'Dr. Paul Myerson', 'Intermediate'),
        ('Agile Project Management', 'Jeremy Jarrell', 'Intermediate'),
        ('Leadership Skills Masterclass', 'Robin Hills', 'Beginner'),
        ('Negotiation Skills', 'Chris Croft', 'Intermediate'),
        ('Productivity Masterclass', 'Ali Abdaal', 'Beginner'),
        ('Six Sigma Green Belt', 'Paul Allen', 'Advanced'),
        ('Business Model Canvas', 'Alexander Osterwalder', 'Intermediate'),
        ('Strategic Planning', 'Michael Porter', 'Advanced'),
        ('Financial Modeling', 'Simon Benninga', 'Advanced'),
    ],
    'Design': [
        ('Graphic Design Masterclass', 'Lindsay Marsh', 'Beginner'),
        ('Adobe Photoshop CC Essentials', 'Daniel Walter Scott', 'Beginner'),
        ('Adobe Illustrator CC Masterclass', 'Daniel Walter Scott', 'Intermediate'),
        ('UI/UX Design Specialization', 'Caleb Atwell', 'Intermediate'),
        ('Figma UI Design', 'Daniel Walter Scott', 'Beginner'),
        ('Web Design for Beginners', 'Brad Schiff', 'Beginner'),
        ('Logo Design Masterclass', 'Lindsay Marsh', 'Intermediate'),
        ('Blender 3D Modeling', 'Grant Abbitt', 'Intermediate'),
        ('After Effects CC Masterclass', 'Phil Ebiner', 'Intermediate'),
        ('InDesign CC Mastery', 'Daniel Walter Scott', 'Intermediate'),
        ('Design Thinking', 'David Kelley', 'Beginner'),
        ('Color Theory Masterclass', 'Lindsay Marsh', 'Beginner'),
        ('Typography Fundamentals', 'Laura Franz', 'Beginner'),
        ('User Experience Design', 'Don Norman', 'Intermediate'),
        ('Sketch App Masterclass', 'Marc Andrew', 'Intermediate'),
    ],
    'Marketing': [
        ('Digital Marketing Masterclass', 'Phil Ebiner', 'Beginner'),
        ('The Complete SEO Course', 'Neil Patel', 'Intermediate'),
        ('Facebook Ads & Marketing', 'Isaac Rudansky', 'Intermediate'),
        ('Google Ads Training', 'Isaac Rudansky', 'Intermediate'),
        ('Email Marketing Masterclass', 'Andre Chaperon', 'Intermediate'),
        ('Social Media Marketing', 'Jay Baer', 'Beginner'),
        ('Content Marketing Strategy', 'Joe Pulizzi', 'Intermediate'),
        ('Instagram Marketing', 'Justin O\'Brien', 'Beginner'),
        ('YouTube Marketing', 'Brian Dean', 'Intermediate'),
        ('Copywriting Secrets', 'Jim Edwards', 'Intermediate'),
        ('Marketing Analytics', 'Avinash Kaushik', 'Advanced'),
        ('Brand Strategy Masterclass', 'Marty Neumeier', 'Intermediate'),
        ('Growth Hacking', 'Sean Ellis', 'Advanced'),
        ('Conversion Rate Optimization', 'Peep Laja', 'Advanced'),
        ('Influencer Marketing', 'Shane Barker', 'Intermediate'),
    ],
    'Data Science': [
        ('Data Science A-Z', 'Kirill Eremenko', 'Beginner'),
        ('Machine Learning with Python', 'Andrew Ng', 'Intermediate'),
        ('Deep Learning Specialization', 'Andrew Ng', 'Advanced'),
        ('Data Analysis with Python', 'Jose Portilla', 'Intermediate'),
        ('Statistics for Data Science', 'Josh Starmer', 'Intermediate'),
        ('R Programming A-Z', 'Kirill Eremenko', 'Beginner'),
        ('SQL for Data Analysis', 'Mode Analytics', 'Beginner'),
        ('Tableau Masterclass', 'Kirill Eremenko', 'Intermediate'),
        ('Power BI Complete Course', 'Maven Analytics', 'Intermediate'),
        ('Big Data and Hadoop', 'Frank Kane', 'Advanced'),
        ('Natural Language Processing', 'Lazy Programmer', 'Advanced'),
        ('Computer Vision A-Z', 'Hadelin de Ponteves', 'Advanced'),
        ('Time Series Analysis', 'Rob J Hyndman', 'Advanced'),
        ('A/B Testing Masterclass', 'Kirill Eremenko', 'Intermediate'),
        ('Data Engineering', 'Frank Kane', 'Advanced'),
    ],
    'Languages': [
        ('Complete Spanish Course', 'Maria Fernandez', 'Beginner'),
        ('French for Beginners', 'Pierre Dubois', 'Beginner'),
        ('Complete German Course', 'Hans Mueller', 'Beginner'),
        ('Mandarin Chinese Complete', 'Li Wei', 'Beginner'),
        ('Japanese for Beginners', 'Yuki Tanaka', 'Beginner'),
        ('Italian Language Masterclass', 'Marco Rossi', 'Beginner'),
        ('Portuguese Complete Course', 'João Silva', 'Beginner'),
        ('Korean Language Course', 'Min-Ji Kim', 'Beginner'),
        ('Arabic for Beginners', 'Ahmed Hassan', 'Beginner'),
        ('Russian Complete Course', 'Natasha Ivanova', 'Beginner'),
        ('English Grammar Masterclass', 'Emma Watson', 'Intermediate'),
        ('Business English', 'Rachel Green', 'Intermediate'),
        ('IELTS Preparation', 'Simon Corcoran', 'Advanced'),
        ('TOEFL Mastery', 'Magoosh Test Prep', 'Advanced'),
        ('Latin Fundamentals', 'Professor Williams', 'Intermediate'),
    ],
    'Music': [
        ('Complete Piano Course', 'Manus Pianoforte', 'Beginner'),
        ('Guitar Lessons Masterclass', 'Erich Andreas', 'Beginner'),
        ('Music Theory Complete', 'Jason Allen', 'Beginner'),
        ('Electronic Music Production', 'Ableton Instructor', 'Intermediate'),
        ('FL Studio Complete Course', 'SeamlessR', 'Intermediate'),
        ('Singing Masterclass', 'Katarina Benzova', 'Beginner'),
        ('Drum Lessons for Beginners', 'Mike Johnston', 'Beginner'),
        ('Ukulele for Absolute Beginners', 'Brett McQueen', 'Beginner'),
        ('Violin Lessons', 'Professor V', 'Beginner'),
        ('Music Composition', 'Jason Allen', 'Intermediate'),
        ('Audio Engineering Complete', 'Recording Revolution', 'Intermediate'),
        ('DJ Mixing Masterclass', 'DJ Carlo Atendido', 'Intermediate'),
        ('Songwriting Secrets', 'Ed Sheeran Masterclass', 'Intermediate'),
        ('Blues Guitar Unleashed', 'Griff Hamlin', 'Intermediate'),
        ('Jazz Piano Complete', 'Willie Myette', 'Advanced'),
    ],
    'Photography': [
        ('Photography Masterclass', 'Phil Ebiner', 'Beginner'),
        ('Smartphone Photography', 'Dale McManus', 'Beginner'),
        ('Portrait Photography', 'Daniel Inskeep', 'Intermediate'),
        ('Landscape Photography', 'Chris Burkard', 'Intermediate'),
        ('Wedding Photography', 'Vanessa Joy', 'Advanced'),
        ('Adobe Lightroom Complete', 'Phil Ebiner', 'Intermediate'),
        ('Food Photography', 'Christina Peters', 'Intermediate'),
        ('Product Photography', 'Jordi Koalitic', 'Intermediate'),
        ('Street Photography', 'Sean Tucker', 'Intermediate'),
        ('Real Estate Photography', 'Nathan Cool', 'Intermediate'),
        ('Night Photography', 'Lance Keimig', 'Advanced'),
        ('Drone Photography', 'Ryan White', 'Intermediate'),
        ('Black and White Photography', 'Ansel Adams Course', 'Advanced'),
        ('Fashion Photography', 'Clay Cook', 'Advanced'),
        ('Wildlife Photography', 'Paul Nicklen', 'Advanced'),
    ],
    'Finance': [
        ('Financial Markets', 'Robert Shiller', 'Beginner'),
        ('Personal Finance Complete', 'Chris Haroun', 'Beginner'),
        ('Stock Trading Complete', 'Mohsen Hassan', 'Intermediate'),
        ('Cryptocurrency Investment', 'Andrei Jikh', 'Intermediate'),
        ('Real Estate Investing', 'BiggerPockets', 'Intermediate'),
        ('Accounting & Bookkeeping', 'Vincenzo Ciaglia', 'Beginner'),
        ('Financial Modeling for Investment Banking', 'Careers in Finance', 'Advanced'),
        ('Options Trading', 'Karen the Trader', 'Advanced'),
        ('Forex Trading', 'Adam Khoo', 'Intermediate'),
        ('Financial Analysis', 'Chris Haroun', 'Intermediate'),
        ('QuickBooks Complete Course', 'Hector Garcia', 'Beginner'),
        ('Excel for Finance', 'Simon Sez IT', 'Intermediate'),
        ('Investment Banking', 'Vikram Barhat', 'Advanced'),
        ('Retirement Planning', 'Bob Carlson', 'Intermediate'),
        ('Tax Preparation', 'Robert Farrington', 'Intermediate'),
    ],
    'Health': [
        ('Yoga for Beginners', 'Adriene Mishler', 'Beginner'),
        ('Complete Meditation Course', 'Giovanni Dienstmann', 'Beginner'),
        ('Nutrition Complete Guide', 'Felix Harder', 'Beginner'),
        ('Weight Training for Beginners', 'Athlean-X', 'Beginner'),
        ('Running & Marathon Training', 'Hal Higdon', 'Intermediate'),
        ('Mental Health & Wellbeing', 'Dr. Andrea Pennington', 'Beginner'),
        ('Sleep Science', 'Dr. Matthew Walker', 'Beginner'),
        ('Mindfulness Based Stress Reduction', 'Jon Kabat-Zinn', 'Beginner'),
        ('Healthy Cooking', 'Gordon Ramsay', 'Beginner'),
        ('CrossFit Training', 'Ben Bergeron', 'Intermediate'),
        ('Pilates Complete', 'Cassey Ho', 'Beginner'),
        ('Sports Psychology', 'Dr. Jim Taylor', 'Intermediate'),
        ('First Aid & CPR', 'Red Cross', 'Beginner'),
        ('Supplements Guide', 'Examine.com', 'Intermediate'),
        ('Keto Diet Complete', 'Dr. Berg', 'Beginner'),
    ]
}

courses = []
course_id = 1

for category, course_list in courses_data.items():
    for title, instructor, difficulty in course_list:
        duration = random.randint(5, 50)  # hours
        rating = round(random.uniform(4.0, 5.0), 1)
        num_students = random.randint(1000, 100000)
        price = random.choice([19.99, 29.99, 49.99, 79.99, 99.99, 149.99])
        
        # Map to match column names in course_recommender.py
        courses.append({
            'course_id': course_id,
            'title': title,
            'instructor': instructor,
            'category': category,
            'subcategory': category,  # Use same as category for simplicity
            'difficulty': difficulty,
            'duration': duration,
            'rating': rating,
            'num_students': num_students,
            'price': price
        })
        course_id += 1

courses_df = pd.DataFrame(courses)
print(f"✓ Generated {len(courses_df)} courses across {len(learning_topics_quiz)} topics")
print(f"  Topic distribution: {courses_df['category'].value_counts().to_dict()}")

# Generate enrollments (35,000 enrollments)
num_enrollments = 35000
enrollments = []

for _ in range(num_enrollments):
    user_id = random.randint(1, num_users)
    course_id = random.randint(1, len(courses_df))
    completion = random.randint(0, 100)
    rating = random.randint(1, 5) if completion > 20 else None
    enrollment_date = datetime.now() - timedelta(days=random.randint(0, 365))
    
    enrollments.append({
        'user_id': user_id,
        'course_id': course_id,
        'progress': completion,  # Changed from 'completion' to 'progress' to match recommender expectations
        'rating': rating,
        'enrollment_date': enrollment_date.strftime('%Y-%m-%d')
    })

enrollments_df = pd.DataFrame(enrollments)
print(f"✓ Generated {len(enrollments_df)} course enrollments")

courses_df.to_csv('../data/courses.csv', index=False)
enrollments_df.to_csv('../data/enrollments.csv', index=False)
print("✓ Course data saved!\n")

# ==================== SUMMARY ====================
print("=" * 60)
print("✅ DATA GENERATION COMPLETE!")
print("=" * 60)
print(f"""
📊 SUMMARY:
   Music:    {len(tracks_df)} tracks across {len(music_genres_quiz)} genres
             {len(listening_df)} listening records
   
   Movies:   Using MovieLens 100K dataset (comprehensive)
   
   Products: {len(products_df)} products across {len(shopping_categories_quiz)} categories
             {len(reviews_df)} reviews
   
   Courses:  {len(courses_df)} courses across {len(learning_topics_quiz)} topics
             {len(enrollments_df)} enrollments

🎯 All quiz options now have MULTIPLE genuine entries!
🎯 Ready for model training!
""")
