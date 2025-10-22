# Hosting LinUtil One-Line Installer

This guide explains how to set up a custom short URL for your LinUtil installer, similar to Chris Titus Tech's `christitus.com/linux`.

## Option 1: Using GitHub Pages (Free)

GitHub automatically serves raw files, so you can use:

```bash
curl -fsSL https://raw.githubusercontent.com/siifat/linutil/main/install.sh | bash
```

### Make it shorter with a custom domain:

1. **Buy a domain** (e.g., `yourname.com` from Namecheap, GoDaddy, etc.)

2. **Set up a redirect page** in your GitHub Pages:

Create `docs/linux` file:
```html
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url=https://raw.githubusercontent.com/siifat/linutil/main/install.sh">
</head>
<body>
    Redirecting to LinUtil installer...
</body>
</html>
```

3. **Configure DNS** to point to GitHub Pages

4. **Your one-liner becomes**:
```bash
curl -fsSL https://yourname.com/linux | bash
```

## Option 2: Using a URL Shortener Service

### Git.io (if still available)
```bash
curl -i https://git.io -F "url=https://raw.githubusercontent.com/siifat/linutil/main/install.sh"
```

### Bit.ly, TinyURL, or Custom Shortener
Create a short link pointing to your raw install.sh URL.

## Option 3: Self-Hosted Server (Full Control)

If you have your own server:

### 1. Set up Nginx redirect

Create `/etc/nginx/sites-available/linutil`:
```nginx
server {
    listen 80;
    server_name yourname.com www.yourname.com;
    
    location /linux {
        return 302 https://raw.githubusercontent.com/siifat/linutil/main/install.sh;
    }
    
    location /linuxdev {
        return 302 https://raw.githubusercontent.com/siifat/linutil/dev/install.sh;
    }
    
    location = / {
        return 302 https://github.com/siifat/linutil;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/linutil /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 2. Add SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourname.com -d www.yourname.com
```

### 3. Your one-liner:
```bash
curl -fsSL https://yourname.com/linux | bash
```

## Option 4: Using Cloudflare Pages (Free + CDN)

1. **Create a Cloudflare account** and add your domain

2. **Create a Pages project** with this structure:
```
public/
├── index.html (redirect to GitHub repo)
├── linux (the install.sh content or redirect)
└── linuxdev (dev branch installer)
```

3. **Set up redirects** in `_redirects` file:
```
/linux    https://raw.githubusercontent.com/siifat/linutil/main/install.sh    302
/linuxdev https://raw.githubusercontent.com/siifat/linutil/dev/install.sh     302
/         https://github.com/siifat/linutil                                   302
```

4. **Deploy** and your URL is ready:
```bash
curl -fsSL https://yourname.com/linux | bash
```

## Option 5: Using Netlify (Free)

1. **Create a Netlify account**

2. **Create `_redirects` file**:
```
/linux    https://raw.githubusercontent.com/siifat/linutil/main/install.sh    302
/linuxdev https://raw.githubusercontent.com/siifat/linutil/dev/install.sh     302
```

3. **Deploy** your site

4. **Your one-liner**:
```bash
curl -fsSL https://yourname.netlify.app/linux | bash
```

Or with custom domain:
```bash
curl -fsSL https://yourname.com/linux | bash
```

## Recommended Setup (What CTT Uses)

Chris Titus Tech likely uses:
- **Custom domain**: christitus.com
- **Simple server/CDN**: Nginx or Cloudflare
- **Multiple endpoints**:
  - `/linux` → stable installer
  - `/linuxdev` → development installer

You can replicate this with **Cloudflare Pages** (easiest + free) or **your own server** (most control).

## Testing Your Setup

1. **Test the URL**:
```bash
curl -fsSL https://yourname.com/linux
```

Should output the install script content.

2. **Test the installer**:
```bash
curl -fsSL https://yourname.com/linux | bash
```

Should install LinUtil.

3. **Test on fresh VM**:
Always test on a clean Linux VM before announcing.

## Security Considerations

1. **Use HTTPS**: Always serve over HTTPS to prevent MITM attacks
2. **Sign your commits**: Use GPG to sign commits
3. **Pin to specific commit**: For production, consider pinning to a release tag
4. **Rate limiting**: Prevent abuse of your installer endpoint
5. **Analytics**: Consider adding download counters

## Marketing Your Installation URL

Update your project to advertise the one-liner:

### README.md
```markdown
## Quick Install
​```bash
curl -fsSL https://yourname.com/linux | bash
​```
```

### Social Media
"Install LinUtil with one command: curl -fsSL https://yourname.com/linux | bash"

### Project Description
"One-command Linux post-install tool"

---

**Choose the option that best fits your needs and budget!**
