const fs = require('fs');

const proxies = [];
const output_file = 'proxy.txt';

if (fs.existsSync(output_file)) {
  fs.unlinkSync(output_file);
  console.log(`'${output_file}' telah dihapus.`);
}

const raw_proxy_sites = [
"https://raw.githubusercontent.com/tuanminpay/live-proxy/master/all.txt",
"https://raw.githubusercontent.com/zevtyardt/proxy-list/main/all.txt",
"https://sunny9577.github.io/proxy-scraper/generated/socks5_proxies.txt",
"https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks5.txt",
"https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/xResults/Proxies.txt",
"https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/xResults/RAW.txt",
"https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt",
"https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5.txt",
"https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text",
];

async function fetchProxies() {
  for (const site of raw_proxy_sites) {
    try {
      const response = await fetch(site);
      if (response.ok) {
//console.log(`success: ${site}`);
        const data = await response.text();
        const lines = data.split('\n');
        for (const line of lines) {
          if (line.includes(':')) {
            const [ip, port] = line.split(':', 2);
            proxies.push(`${ip}:${port}`);
          }
        }
      } else {
//console.log(`skip: ${site}`);
      }
    } catch (error) {
//console.error(`skip: ${site}`);
    }
  }

  fs.writeFileSync(output_file, proxies.join('\n'));
  fs.readFile(output_file, 'utf8', (err, data) => {
    if (err) {
      console.error('Gagal membaca file:', err);
      return;
    }
    const proxies = data.trim().split('\n');
    const totalProxies = proxies.length;
    console.log(`success scraping ${totalProxies} proxy`);
  });
}
fetchProxies();
