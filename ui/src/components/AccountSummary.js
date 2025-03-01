import React from 'react';
import { Box, Flex, Text, Stat, StatLabel, StatNumber, StatHelpText, Badge, useColorModeValue, Icon } from '@chakra-ui/react';
import { FaUser, FaCoins } from 'react-icons/fa';

const AccountSummary = ({ accountId, balance }) => {
  const cardBg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  const iconColor = useColorModeValue('near.primary', 'near.secondary');

  return (
    <Box 
      p={5} 
      borderRadius="xl" 
      bg={cardBg} 
      boxShadow="md" 
      borderWidth="1px" 
      borderColor={borderColor}
    >
      <Flex justifyContent="space-between" alignItems="center" mb={4}>
        <Text fontSize="xl" fontWeight="bold">Account Overview</Text>
        <Badge colorScheme="green" fontSize="0.8em" p={2} borderRadius="md">
          Active
        </Badge>
      </Flex>

      <Flex direction={["column", "row"]} gap={8}>
        <Stat>
          <Flex alignItems="center">
            <Icon as={FaUser} mr={2} color={iconColor} />
            <StatLabel>Account ID</StatLabel>
          </Flex>
          <StatNumber fontSize="lg">{accountId}</StatNumber>
          <StatHelpText>NEAR Blockchain</StatHelpText>
        </Stat>

        <Stat>
          <Flex alignItems="center">
            <Icon as={FaCoins} mr={2} color={iconColor} />
            <StatLabel>Available Balance</StatLabel>
          </Flex>
          <StatNumber fontSize="lg">{balance.toFixed(2)} NEAR</StatNumber>
          <StatHelpText>
            ~${(balance * 3.45).toFixed(2)} USD
          </StatHelpText>
        </Stat>
      </Flex>
    </Box>
  );
};

export default AccountSummary; 