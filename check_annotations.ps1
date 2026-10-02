$root = Get-Location
$csvPath = Join-Path $root "annotations\expert_1.csv"
$outPath = Join-Path $root "annotation_check_report.csv"

$annotations = Import-Csv $csvPath
$results = @()

function Get-BenchmarkFile {
    param(
        [string]$FileId
    )

    $terraform = Get-ChildItem (Join-Path $root "benchmark\terraform") -Recurse -Filter "main.tf" |
        Where-Object { $_.FullName -match "\\$FileId\\main\.tf$" }

    if ($terraform) {
        return @{
            Path   = $terraform.FullName
            Format = "terraform"
        }
    }

    $cloudformation = Get-ChildItem (Join-Path $root "benchmark\cloudformation") -Recurse -Filter "main.yaml" |
        Where-Object { $_.FullName -match "\\$FileId\\main\.yaml$" }

    if (-not $cloudformation) {
        $cloudformation = Get-ChildItem (Join-Path $root "benchmark\cloudformation") -Recurse -Filter "main.yml" |
            Where-Object { $_.FullName -match "\\$FileId\\main\.yml$" }
    }

    if ($cloudformation) {
        return @{
            Path   = $cloudformation.FullName
            Format = "cloudformation"
        }
    }

    return $null
}

function Test-Policy {
    param(
        [string]$Policy,
        [string]$Content,
        [string]$Format
    )

    switch -Regex ($Policy) {

        "POL_AWS_S3_PUBLIC" {
            if ($Content -match '(?i)\bacl\s*=\s*"public-read"') {
                return $true
            }

            if ($Content -match '(?i)(PublicRead|public-read|PublicReadWrite|public-read-write)') {
                return $true
            }

            return $false
        }

        "POL_AWS_RDS_PUBLIC" {
            if ($Content -match '(?i)\bpublicly_accessible\s*=\s*true\b') {
                return $true
            }

            if ($Content -match '(?i)PubliclyAccessible\s*:\s*true\b') {
                return $true
            }

            return $false
        }

        "POL_AWS_RDS_ENCRYPTION" {
            if ($Content -match '(?i)\bstorage_encrypted\s*=\s*true\b') {
                return $false
            }

            if ($Content -match '(?i)\bstorage_encrypted\s*=\s*false\b') {
                return $true
            }

            if ($Content -match '(?i)StorageEncrypted\s*:\s*false\b') {
                return $true
            }

            if ($Content -match '(?i)StorageEncrypted\s*:\s*true\b') {
                return $false
            }

            return $null
        }

        "POL_AWS_SG_UNRESTRICTED" {
            if ($Content -match '(?i)cidr_blocks\s*=\s*\[\s*"0\.0\.0\.0/0"\s*\]') {
                return $true
            }

            if ($Content -match '(?i)CidrIp\s*:\s*["'']0\.0\.0\.0/0["'']') {
                return $true
            }

            return $false
        }

        "POL_AWS_IAM_WILDCARD" {
            if ($Content -match '(?i)"\*"') {
                return $true
            }

            if ($Content -match "(?i)'\\*'") {
                return $true
            }

            return $false
        }

        default {
            return $null
        }
    }
}

foreach ($row in $annotations) {

    $file = Get-BenchmarkFile $row.file_id

    if (-not $file) {
        $results += [PSCustomObject]@{
            file_id        = $row.file_id
            policy_sid     = $row.policy_sid
            annotation     = "FILE_NOT_FOUND"
            detected       = ""
            status         = "ERROR"
            resource_id    = $row.resource_id
            severity       = $row.severity
        }
        continue
    }

    $content = Get-Content $file.Path -Raw

    $detected = Test-Policy `
        -Policy $row.policy_sid `
        -Content $content `
        -Format $file.Format

    if ($null -eq $detected) {
        $status = "MANUAL_REVIEW"
        $detectedText = "UNKNOWN"
    }
    elseif ($detected -eq $true) {
        $status = "MATCH"
        $detectedText = "VIOLATION_PRESENT"
    }
    else {
        $status = "MISMATCH"
        $detectedText = "VIOLATION_NOT_PRESENT"
    }

    $results += [PSCustomObject]@{
        file_id        = $row.file_id
        instance_id    = $row.instance_id
        format         = $row.format
        resource_id    = $row.resource_id
        policy_sid     = $row.policy_sid
        severity       = $row.severity
        detected       = $detectedText
        status         = $status
        reviewer_label = $row.reviewer_label
        reviewer_notes = $row.reviewer_notes
        source_file    = $file.Path
    }
}

$results | Export-Csv $outPath -NoTypeInformation -Encoding UTF8

Write-Host ""
Write-Host "========================================"
Write-Host " CloudGuard Annotation Consistency Check"
Write-Host "========================================"
Write-Host ""

$results | Group-Object status | Format-Table Name,Count -AutoSize

Write-Host ""
Write-Host "MISMATCHES:"
Write-Host ""

$results |
    Where-Object { $_.status -eq "MISMATCH" } |
    Format-Table file_id, policy_sid, severity, detected -AutoSize

Write-Host ""
Write-Host "Report saved to:"
Write-Host $outPath
