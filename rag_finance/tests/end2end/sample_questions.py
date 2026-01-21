import json
import urllib.request
import urllib.error

SAMPLE_QUESTIONS = [
    "Quais foram os meus principais gastos este mês?",
    "Qual foi o valor total da fatura?",
    "Quanto gastei de IOF?",
    "Quais foram os itens mais caros da minha fatura?",
    "Quais foram os itens mais baratos da minha fatura?",
    "Quais foram os itens mais frequentes na minha fatura?",
]


def test_message_endpoint(base_url: str = "http://localhost:8000"):
    """
    Test the message endpoint with all sample questions.
    Assert that all responses return 202 status code.
    
    Args:
        base_url: Base URL of the FastAPI application
    """
    endpoint_url = f"{base_url}/message"
    results = []
    
    print(f"Testing message endpoint at: {endpoint_url}")
    print(f"Number of questions to test: {len(SAMPLE_QUESTIONS)}")
    print("-" * 50)
    
    for i, question in enumerate(SAMPLE_QUESTIONS, 1):
        try:
            # Prepare request data
            data = {'question': question}
            json_data = json.dumps(data).encode('utf-8')
            
            # Create request
            req = urllib.request.Request(endpoint_url, data=json_data)
            req.add_header('Content-Type', 'application/json')
            
            # Make request
            response = urllib.request.urlopen(req)
            status_code = response.getcode()
            response_data = json.loads(response.read().decode('utf-8'))
            
            # Assert status code is 202
            assert status_code == 202, f"Expected 202, got {status_code} for question: {question}"
            
            # Log successful test
            print(f"✓ Test {i}/{len(SAMPLE_QUESTIONS)}: Status {status_code}")
            print(f"  Question: {question[:50]}...")
            print(f"  Task ID: {response_data.get('task_id', 'N/A')}")
            print(f"  Status: {response_data.get('status', 'N/A')}")
            
            results.append({
                'question': question,
                'status_code': status_code,
                'response': response_data,
                'success': True
            })
            
        except urllib.error.HTTPError as e:
            error_msg = f"HTTP Error {e.code}: {e.reason}"
            print(f"✗ Test {i}/{len(SAMPLE_QUESTIONS)}: {error_msg}")
            print(f"  Question: {question}")
            
            results.append({
                'question': question,
                'status_code': e.code,
                'error': error_msg,
                'success': False
            })
            
            # Assert failure
            assert False, f"HTTP Error {e.code} for question: {question}"
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(f"✗ Test {i}/{len(SAMPLE_QUESTIONS)}: {error_msg}")
            print(f"  Question: {question}")
            
            results.append({
                'question': question,
                'error': error_msg,
                'success': False
            })
            
            # Assert failure
            assert False, f"Unexpected error for question: {question}"
        
    
    # Summary
    successful_tests = sum(1 for r in results if r['success'])
    print("-" * 50)
    print(f"Test Summary: {successful_tests}/{len(SAMPLE_QUESTIONS)} tests passed")
    
    if successful_tests == len(SAMPLE_QUESTIONS):
        print("🎉 All tests passed! All endpoints returned 202 status code.")
    else:
        print("❌ Some tests failed!")
    
    return results


if __name__ == "__main__":
    # Run the tests
    test_message_endpoint()