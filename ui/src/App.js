import React, { useState, useEffect, useRef } from 'react';
import { ChakraProvider, Box, Container, Text, Heading, VStack, useColorModeValue, IconButton } from '@chakra-ui/react';
import { FaComments } from 'react-icons/fa';
import { mockData } from './mockData';
import AccountSummary from './components/AccountSummary';
import StakingRecommendation from './components/StakingRecommendation';
import TransactionHistory from './components/TransactionHistory';
import theme from './theme';

function App() {
  const [isChatVisible, setIsChatVisible] = useState(false);
  const iframeRef = useRef(null);
  const intervalRef = useRef(null);

  const { accountId, balance, recommendation, transactions } = mockData;

  const bgColor = useColorModeValue('gray.50', 'gray.900');
  const headerBgColor = useColorModeValue('blue.600', 'blue.200');
  const headerColor = useColorModeValue('white', 'gray.800');

  const handleChatToggle = () => {
    setIsChatVisible(!isChatVisible);
  };

  useEffect(() => {
    const fetchIframeContent = () => {
      try {


        console.log(iframeRef.current.contentWindow.document.body.innerHTML);

        // const elements = iframeRef.current.querySelectorAll('[class^="Markdown_markdown__HGPnT"]')

        // console.log(elements);

      } catch (error) {
        console.error("Error accessing iframe content: ", error);
      }
    };

    if (isChatVisible) {
      intervalRef.current = setInterval(fetchIframeContent, 5000); // Fetch every 2 seconds
    } else {
      clearInterval(intervalRef.current);
    }

    return () => clearInterval(intervalRef.current);
  }, [isChatVisible]);

  return (
    <ChakraProvider theme={theme}>
      <Box position="relative">
        {isChatVisible && (
          <iframe
            ref={iframeRef}
            src="https://app.near.ai/embed/sachinanand.near/DefiShield/latest"
            sandbox="allow-scripts allow-popups allow-same-origin allow-forms"
            title="DefiShield"
            style={{
              border: 'none',
              height: '100vh',
              width: '30%',
              position: 'fixed',
              top: 0,
              right: 0,
              zIndex: 1000,
              transition: 'transform 0.3s ease-in-out',
              transform: isChatVisible ? 'translateX(0)' : 'translateX(100%)',
            }}
          />
        )}
        <Box
          bg={bgColor}
          minH="100vh"
          py={5}
          transition="margin-right 0.3s ease-in-out"
          mr={isChatVisible ? '30%' : '0'}
        >
          <Box bg={headerBgColor} color={headerColor} py={4} mb={6} textAlign="center">
            <Heading as="h1" size="xl">DefiShield</Heading>
            <Text mt={1}>AI-powered DeFi monitoring and recommendations</Text>
          </Box>

          <Container maxW="container.lg">
            <VStack spacing={8} align="stretch">
              <AccountSummary accountId={accountId} balance={balance} />
              <StakingRecommendation recommendation={recommendation} />
              <TransactionHistory transactions={transactions} />
            </VStack>
          </Container>
        </Box>
        <IconButton
          icon={<FaComments />}
          colorScheme="teal"
          position="fixed"
          bottom="20px"
          right="20px"
          borderRadius="full"
          boxShadow="lg"
          onClick={handleChatToggle}
          zIndex={1001}
        />
      </Box>
    </ChakraProvider>
  );
}

export default App;
