# run_all.ps1

$HostUrl = 'http://localhost:5000'
$LongUrl = 'https://example.com/very/long/path'

Write-Host "=== Health Check (GET /) ==="
Invoke-RestMethod -Uri "$HostUrl/" | ConvertTo-Json -Depth 4
Write-Host ''

Write-Host "=== API Health (GET /api/health) ==="
Invoke-RestMethod -Uri "$HostUrl/api/health" | ConvertTo-Json -Depth 4
Write-Host ''

Write-Host "=== Shorten URL (POST /api/shorten) ==="
$body = @{ url = $LongUrl } | ConvertTo-Json
$resp = Invoke-RestMethod -Method Post -Uri "$HostUrl/api/shorten" -Body $body -ContentType 'application/json'
$resp | ConvertTo-Json -Depth 4
Write-Host ''

$code = $resp.short_code
Write-Host "Extracted short code: $code"
Write-Host ''

Write-Host "=== Redirect (GET /$code) without auto‑follow ==="
# Create a .NET HttpWebRequest, turn off AutoRedirect
$req = [System.Net.WebRequest]::Create("$HostUrl/$code")
$req.Method = 'GET'
# Cast to HttpWebRequest so we can set AllowAutoRedirect
$httpReq = [System.Net.HttpWebRequest]$req
$httpReq.AllowAutoRedirect = $false

try {
    $res = $httpReq.GetResponse()
    # If somehow it didn't redirect, print content or status
    Write-Host "StatusCode: $($res.StatusCode.value__)"
    $res.Close()
}
catch [System.Net.WebException] {
    $raw = $_.Response
    Write-Host "StatusCode: $($raw.StatusCode.value__)"
    Write-Host "Location:   $($raw.Headers['Location'])"
    $raw.Close()
}
Write-Host ''

Write-Host "=== Stats (GET /api/stats/$code) ==="
Invoke-RestMethod -Uri "$HostUrl/api/stats/$code" | ConvertTo-Json -Depth 4
