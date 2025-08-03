"""
Azure OpenAI Configuration Helper
This script helps you configure your Azure OpenAI settings.
"""

import os
from dotenv import load_dotenv

def configure_azure_openai():
    """Help configure Azure OpenAI settings."""
    
    print("🔧 Azure OpenAI Configuration Helper")
    print("=" * 50)
    
    print("To use Azure OpenAI, you need to provide:")
    print("1. Azure OpenAI API Key (you already have this)")
    print("2. Azure OpenAI Endpoint URL")
    print("3. Deployment name for your GPT-4 model")
    print()
    
    # Load current .env
    load_dotenv()
    current_key = os.getenv("AZURE_OPENAI_API_KEY", "")
    
    print("Current configuration:")
    print(f"✅ API Key: {'*' * 20}{current_key[-10:] if current_key else 'Not set'}")
    print(f"⚠️  Endpoint: {os.getenv('AZURE_OPENAI_ENDPOINT', 'NEEDS CONFIGURATION')}")
    print(f"⚠️  Deployment: {os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', 'NEEDS CONFIGURATION')}")
    print()
    
    print("📝 To complete your Azure OpenAI setup:")
    print()
    print("1. Find your Azure OpenAI endpoint:")
    print("   - Go to https://portal.azure.com")
    print("   - Navigate to your Azure OpenAI resource")
    print("   - Copy the 'Endpoint' URL (e.g., https://your-resource.openai.azure.com/)")
    print()
    print("2. Find your deployment name:")
    print("   - In Azure OpenAI Studio (https://oai.azure.com/)")
    print("   - Go to 'Deployments' section")
    print("   - Copy the name of your GPT-4 deployment")
    print()
    print("3. Update your .env file with these values:")
    print("   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/")
    print("   AZURE_OPENAI_DEPLOYMENT_NAME=your-gpt4-deployment-name")
    print()
    
    return True

def test_azure_config():
    """Test Azure OpenAI configuration."""
    
    load_dotenv()
    
    required_vars = [
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT", 
        "AZURE_OPENAI_DEPLOYMENT_NAME"
    ]
    
    print("🧪 Testing Azure OpenAI Configuration")
    print("=" * 50)
    
    all_configured = True
    for var in required_vars:
        value = os.getenv(var)
        if value and value != "your-resource-name.openai.azure.com/" and value != "gpt-4":
            print(f"✅ {var}: Configured")
        else:
            print(f"❌ {var}: Not configured or using placeholder")
            all_configured = False
    
    if all_configured:
        print("\n✅ Azure OpenAI configuration looks complete!")
        print("🚀 You can now test with: python hackathon_test.py")
    else:
        print("\n⚠️  Please complete the Azure OpenAI configuration")
        print("📖 Follow the instructions above to get your endpoint and deployment name")
    
    return all_configured

if __name__ == "__main__":
    configure_azure_openai()
    print()
    test_azure_config()
