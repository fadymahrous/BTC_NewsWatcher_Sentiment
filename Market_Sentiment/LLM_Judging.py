import boto3
from botocore.exceptions import ClientError

class LLMJudging:
    def __init__(self,region_name:str='eu-central-1'):        
        #define our clients
        self.region_name=region_name
        self.chat_client = boto3.client("bedrock-runtime", region_name=self.region_name)
        self.client = boto3.client("bedrock", region_name=self.region_name)


    def _get_model_ARN_interface(self,part_of_model_string:str):
        """This method is used to look up the interface beased on the string passed"""
        arn_interfaces_list=[]
        response = self.client.list_inference_profiles(
            maxResults=123,
            typeEquals='SYSTEM_DEFINED'
        )
        for arn_interface in response.get('inferenceProfileSummaries',[]):
            arn_interfaces_list.append(arn_interface.get('inferenceProfileArn',''))

        # If the response has a nextToken, use it in the next call
        while 'nextToken' in response:
            next_token = response['nextToken']
            response = self.client.list_inference_profiles(
                maxResults=123,
                nextToken=next_token,
                typeEquals='SYSTEM_DEFINED'
            )
            for arn_interface in response.get('inferenceProfileSummaries',[]):
                arn_interfaces_list.append(arn_interface.get('inferenceProfileArn',''))
        for arn_interface in arn_interfaces_list:
            if part_of_model_string.lower() in arn_interface.lower():
                return arn_interface
        return None


    def send_message(self,part_of_model_string:str,user_message: str) -> str:
        #Check model exist string is provided and will be used for loog up later
        if part_of_model_string is None:
            raise ValueError("you must pase part of the model name to look for it")
        #Get Model  ARN from Amazon Bed Rock and if not exist raise Error       
        self.model_id=self._get_model_ARN_interface(part_of_model_string)
        if self.model_id is None:
            return "Model_Not_Exist"


        prompt='''Please answer with “Yes” or “No” only. Do not do any analysis or explanation.
                    Question:
                    Is the following statement a red flag indicating that investors should temporarily sell Bitcoin until the downtrend ends, and then buy again?
                    Statement:'''
        conversation = [
            {
                "role": "user",
                "content": [{"text": prompt+user_message}],
            }
        ]

        try:
            response = self.chat_client.converse(
                modelId=self.model_id,
                messages=conversation,
                inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
            )

            response_text = response["output"]["message"]["content"][0]["text"]
            return response_text

        except (ClientError, Exception) as e:
            raise RuntimeError(f"ERROR: Can't invoke '{self.model_id}'. Reason: {e}") from e

if __name__ == "__main__":
    judge = LLMJudging()
    reply = judge.send_message('sonnet-4',"Hello! Can you help me?")
    print("Model response:", reply)
