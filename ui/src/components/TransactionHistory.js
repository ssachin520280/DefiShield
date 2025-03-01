import React from 'react';
import { 
  Box, 
  Text, 
  Heading, 
  Flex, 
  Table, 
  Thead, 
  Tbody, 
  Tr, 
  Th, 
  Td, 
  Badge, 
  Link, 
  Icon,
  useColorModeValue 
} from '@chakra-ui/react';
import { FaExchangeAlt, FaExternalLinkAlt } from 'react-icons/fa';

const TransactionHistory = ({ transactions }) => {
  const cardBg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  const iconColor = useColorModeValue('near.primary', 'near.secondary');
  const hoverBg = useColorModeValue('gray.50', 'gray.700');

  // Format timestamp to readable date
  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleDateString(undefined, { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  // Get badge color based on transaction type
  const getTypeColor = (type) => {
    const typeMap = {
      'transfer': 'purple',
      'stake': 'green',
      'unstake': 'orange',
      'swap': 'blue',
      'call': 'cyan',
      'deploy': 'pink'
    };
    return typeMap[type.toLowerCase()] || 'gray';
  };

  return (
    <Box 
      p={5} 
      borderRadius="xl" 
      bg={cardBg} 
      boxShadow="md" 
      borderWidth="1px" 
      borderColor={borderColor}
    >
      <Flex alignItems="center" mb={4}>
        <Icon as={FaExchangeAlt} mr={3} color={iconColor} fontSize="xl" />
        <Heading as="h2" size="lg">Recent Transactions</Heading>
      </Flex>

      <Box overflowX="auto">
        <Table variant="simple">
          <Thead>
            <Tr>
              <Th>Type</Th>
              <Th>Date</Th>
              <Th>Details</Th>
              <Th isNumeric>Amount</Th>
              <Th>Status</Th>
              <Th>Explorer</Th>
            </Tr>
          </Thead>
          <Tbody>
            {transactions.map((tx, index) => (
              <Tr 
                key={index}
                _hover={{ bg: hoverBg }}
                transition="background 0.2s"
              >
                <Td>
                  <Badge colorScheme={getTypeColor(tx.type)} px={2} py={1} borderRadius="md">
                    {tx.type}
                  </Badge>
                </Td>
                <Td>{formatDate(tx.timestamp)}</Td>
                <Td>
                  {tx.details ? (
                    tx.details
                  ) : (
                    <>
                      {tx.from && tx.to ? (
                        <Text fontSize="sm">
                          {tx.from} → {tx.to}
                        </Text>
                      ) : (
                        <Text fontSize="sm" color="gray.500">N/A</Text>
                      )}
                    </>
                  )}
                </Td>
                <Td isNumeric fontWeight="medium">
                  {tx.amount ? `${tx.amount} NEAR` : '—'}
                </Td>
                <Td>
                  <Badge 
                    colorScheme={tx.status === 'Success' ? 'green' : tx.status === 'Pending' ? 'yellow' : 'red'}
                    variant="subtle"
                    px={2}
                    py={1}
                  >
                    {tx.status}
                  </Badge>
                </Td>
                <Td>
                  <Link 
                    href={`https://explorer.near.org/transactions/${tx.hash}`} 
                    isExternal
                    color={iconColor}
                    _hover={{ textDecoration: 'none', color: 'blue.500' }}
                  >
                    <Flex alignItems="center">
                      <Text mr={1} fontSize="sm">View</Text>
                      <Icon as={FaExternalLinkAlt} fontSize="xs" />
                    </Flex>
                  </Link>
                </Td>
              </Tr>
            ))}
          </Tbody>
        </Table>
      </Box>
    </Box>
  );
};

export default TransactionHistory; 