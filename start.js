var express = require('express');
var session = require('express-session');
var passport = require('passport');
var BnetStrategy = require('passport-bnet').Strategy;
var app = express();

require('dotenv').config();

var BNET_ID = process.env.BNET_ID;
var BNET_SECRET = process.env.BNET_SECRET;
var SESSION_SECRET = process.env.SESSION_SECRET;

if (!BNET_ID || !BNET_SECRET || !SESSION_SECRET) {
    throw new Error("Missing required environment variables. Please check your .env file.");
}

app.use(session({ secret: SESSION_SECRET, resave: false, saveUninitialized: true }));
app.use(passport.initialize());
app.use(passport.session());

passport.use(new BnetStrategy({
    clientID: BNET_ID,
    clientSecret: BNET_SECRET,
    callbackURL: "https://dev.battle.net/auth/bnet/callback",
    region: "us"
}, function(accessToken, refreshToken, profile, done) {
    profile.accessToken = accessToken;
    return done(null, profile);
}));

passport.serializeUser(function(user, done) {
    done(null, user);
});

passport.deserializeUser(function(obj, done) {
    done(null, obj);
});

app.get('/auth/bnet',
    passport.authenticate('bnet'));

app.get('/auth/bnet/callback',
    passport.authenticate('bnet', { failureRedirect: '/' }),
    function(req, res) {
        res.redirect('/');
    });

app.get('/profile', (req, res) => {
    if (req.isAuthenticated()) {
        res.json({ accessToken: req.user.accessToken });
    } else {
        res.status(401).json({ error: 'Not authenticated' });
    }
});

app.listen(3000, function() {
    console.log('Server running on https://localhost:3000');
});


