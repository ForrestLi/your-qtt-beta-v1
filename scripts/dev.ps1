# Colors for output
$ErrorActionPreference = "Stop"

function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    else {
        $input | Write-Output
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

# Function to display help
function Show-Help {
    Write-ColorOutput Yellow "Usage: .\dev.ps1 [command]"
    Write-Output ""
    Write-Output "Available commands:"
    Write-Output "  start          Start all services in development mode"
    Write-Output "  stop           Stop all services"
    Write-Output "  restart        Restart all services"
    Write-Output "  logs           Show logs for all services"
    Write-Output "  backend        Run backend commands"
    Write-Output "  frontend       Run frontend commands"
    Write-Output "  db             Database management commands"
    Write-Output "  test           Run tests"
    Write-Output "  help           Show this help message"
    Write-Output ""
    Write-Output "Examples:"
    Write-Output "  .\dev.ps1 start"
    Write-Output "  .\dev.ps1 backend migrate"
    Write-Output "  .\dev.ps1 frontend dev"
}

# Function to start services
function Start-Services {
    Write-ColorOutput Green "Starting development services..."
    docker-compose up -d
    Write-ColorOutput Green "Services started!"
    Write-ColorOutput Yellow "Frontend: http://localhost:5173"
    Write-ColorOutput Yellow "Backend API: http://localhost:8000"
    Write-ColorOutput Yellow "API Docs: http://localhost:8000/docs"
}

# Function to stop services
function Stop-Services {
    Write-ColorOutput Yellow "Stopping services..."
    docker-compose down
    Write-ColorOutput Green "Services stopped."
}

# Function to restart services
function Restart-Services {
    Stop-Services
    Start-Services
}

# Function to show logs
function Show-Logs {
    docker-compose logs -f
}

# Function to handle backend commands
function Invoke-BackendCommand {
    param (
        [string]$Command,
        [string]$Message = $null
    )

    switch ($Command) {
        "migrate" {
            Write-ColorOutput Green "Running database migrations..."
            docker-compose exec backend alembic upgrade head
        }
        "migrations" {
            Write-ColorOutput Green "Creating new migration..."
            docker-compose exec backend alembic revision --autogenerate -m $Message
        }
        "shell" {
            docker-compose exec backend bash
        }
        "test" {
            docker-compose exec backend pytest
        }
        default {
            Write-ColorOutput Red "Unknown backend command: $Command"
            Write-Output ""
            Write-Output "Available backend commands:"
            Write-Output "  migrate       Apply database migrations"
            Write-Output "  migrations    Create new migration"
            Write-Output "  shell         Open shell in backend container"
            Write-Output "  test          Run backend tests"
        }
    }
}

# Function to handle frontend commands
function Invoke-FrontendCommand {
    param (
        [string]$Command
    )

    $frontendPath = Join-Path $PSScriptRoot "..\frontend" -Resolve

    switch ($Command) {
        "dev" {
            Write-ColorOutput Green "Starting frontend development server..."
            Set-Location $frontendPath
            npm run dev
        }
        "build" {
            Write-ColorOutput Green "Building frontend for production..."
            Set-Location $frontendPath
            npm run build
        }
        "test" {
            Set-Location $frontendPath
            npm run test
        }
        "lint" {
            Set-Location $frontendPath
            npm run lint
        }
        default {
            Write-ColorOutput Red "Unknown frontend command: $Command"
            Write-Output ""
            Write-Output "Available frontend commands:"
            Write-Output "  dev     Start development server"
            Write-Output "  build   Build for production"
            Write-Output "  test    Run tests"
            Write-Output "  lint    Run linter"
        }
    }
}

# Function to handle database commands
function Invoke-DatabaseCommand {
    param (
        [string]$Command,
        [string]$BackupFile = $null
    )

    $envPath = Join-Path $PSScriptRoot "..\.env" -Resolve
    $envContent = Get-Content $envPath -Raw
    $envVars = @{}
    
    # Parse .env file
    $envContent -split "`n" | ForEach-Object {
        if ($_ -match '^([^#][^=]+)=(.*)') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim('"\'').Trim()
            $envVars[$key] = $value
        }
    }

    $dbUser = $envVars["POSTGRES_USER"]
    $dbName = $envVars["POSTGRES_DB"]
    $dbPassword = $envVars["POSTGRES_PASSWORD"]

    switch ($Command) {
        "reset" {
            Write-ColorOutput Yellow "Resetting database..."
            docker-compose down -v
            docker-compose up -d postgres redis
            # Wait for postgres to start
            Start-Sleep -Seconds 5
            docker-compose exec backend python -m scripts.init_db
        }
        "backup" {
            $backupFile = if ($BackupFile) { $BackupFile } else { "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').sql" }
            Write-ColorOutput Green "Creating database backup to $backupFile..."
            $env:PGPASSWORD = $dbPassword
            docker-compose exec -T postgres pg_dump -U $dbUser -d $dbName > $backupFile
            Write-ColorOutput Green "Backup created: " -NoNewline
            Write-ColorOutput Yellow $backupFile
        }
        default {
            Write-ColorOutput Red "Unknown database command: $Command"
            Write-Output ""
            Write-Output "Available database commands:"
            Write-Output "  reset     Reset database and run migrations"
            Write-Output "  backup    Create database backup"
        }
    }
}

# Function to run tests
function Invoke-TestCommand {
    Write-ColorOutput Green "Running tests..."
    
    # Run backend tests
    Write-ColorOutput Yellow "Backend Tests:"
    docker-compose exec backend pytest
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    
    # Run frontend tests
    Write-ColorOutput Yellow "Frontend Tests:"
    $frontendPath = Join-Path $PSScriptRoot "..\frontend" -Resolve
    Set-Location $frontendPath
    npm run test
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

# Main script execution
$command = $args[0]
$subCommand = $args[1]
$message = $args[2..$args.Length] -join ' '

switch ($command) {
    "start" { Start-Services }
    "stop" { Stop-Services }
    "restart" { Restart-Services }
    "logs" { Show-Logs }
    "backend" { Invoke-BackendCommand -Command $subCommand -Message $message }
    "frontend" { Invoke-FrontendCommand -Command $subCommand }
    "db" { Invoke-DatabaseCommand -Command $subCommand -BackupFile $message }
    "test" { Invoke-TestCommand }
    { @("help", "--help", "-h", "") -contains $_ } { Show-Help }
    default {
        if ($command) {
            Write-ColorOutput Red "Unknown command: $command"
        }
        Show-Help
        exit 1
    }
}

exit 0
