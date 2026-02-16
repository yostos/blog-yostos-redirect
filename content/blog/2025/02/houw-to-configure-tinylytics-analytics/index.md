+++
title = "How to Configure Tinylytics Analytics for Production Environment Only"
description = "I have tried to prevent tinylytics stats from being retrieved outside of the production environment."
date = 2025-02-25
aliases = ["/articles/2025/02/25/houw-to-configure-tinylytics-analytics"]

[taxonomies]
tags = ["Tech","Weblog"]
[extra]
social_media_card = "ogp.webp"
+++

## Why is this code needed?

When incorporating tinylytics javascript, accesses during development are also reflected in the statistics, so we added code so that statistics are obtained only in production. There may be a better way to do this, but for now, I'll introduce it here because it does what I want to do.

## How this code works

This code works as follows:

1. When the page loads, JavaScript checks the current hostname (domain)
2. Only if the hostname exactly matches "your.domain.com", it will add the tinylytics script
3. For all other domains (such as localhost or staging environments), the script won't be added. Only a console message will be displayed

## Implementation

Place this code in the &lt;head&gt; section of your HTML and remove the original tinylytics script tag.

```javascript
<!-- Check domain and enable analytics only for specific domain -->
<script>
  // Get current hostname
  const currentHostname = window.location.hostname;

  // Specify production domain
  const productionDomain = 'your.domain.com';

  // Only load analytics on production domain
  if (currentHostname === productionDomain) {
    // Dynamically add tinylytics script
    const analyticScript = document.createElement('script');
    analyticScript.src = 'https://tinylytics.app/embed/Xx-xxxxxxxxxxxxxx.js';
    analyticScript.defer = true;
    document.head.appendChild(analyticScript);
    console.log('Production environment: Analytics enabled');
  } else {
    console.log('Development environment: Analytics disabled');
  }
</script>
```
