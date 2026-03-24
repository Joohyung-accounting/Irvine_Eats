BEGIN TRANSACTION;

ALTER TABLE restaurants RENAME TO restaurants_old;

CREATE TABLE restaurants (
  restaurant_id INTEGER PRIMARY KEY AUTOINCREMENT,
  place_id TEXT UNIQUE,          
  name TEXT NOT NULL,
  address TEXT,                  
  hours TEXT DEFAULT '',         
  category TEXT DEFAULT 'restaurant',
  phone TEXT,                    
  url TEXT                       
);

INSERT INTO restaurants (restaurant_id, name, address, hours, category, phone, url)
SELECT restaurant_id, name, address, hours, category, phone, url
FROM restaurants_old;

DROP TABLE restaurants_old;

CREATE TABLE IF NOT EXISTS favorite_restaurants (
  user_id INTEGER NOT NULL,
  restaurant_id INTEGER NOT NULL,
  PRIMARY KEY (user_id, restaurant_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id) ON DELETE CASCADE
);

COMMIT;
