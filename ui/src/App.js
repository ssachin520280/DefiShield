import React from 'react';
import { ChakraProvider, Box, Container, Text, Heading, VStack, useColorModeValue } from '@chakra-ui/react';
import { mockData } from './mockData';
import AccountSummary from './components/AccountSummary';
import StakingRecommendation from './components/StakingRecommendation';
import TransactionHistory from './components/TransactionHistory';
import theme from './theme';

function App() {
  // In a real app, you would fetch data from an API endpoint
  // For now, we're using the mock data
  const { accountId, balance, recommendation, transactions } = mockData;
  
  const bgColor = useColorModeValue('gray.50', 'gray.900');
  const headerBgColor = useColorModeValue('blue.600', 'blue.200');
  const headerColor = useColorModeValue('white', 'gray.800');

  return (
    <ChakraProvider theme={theme}>
      <Box bg={bgColor} minH="100vh" py={5}>
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
    </ChakraProvider>
  );
}

export default App; 