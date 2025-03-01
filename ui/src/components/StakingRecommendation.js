import React from 'react';
import { 
  Box, 
  Text, 
  Heading, 
  VStack, 
  HStack, 
  Flex, 
  Progress, 
  Badge, 
  Table, 
  Thead, 
  Tbody, 
  Tr, 
  Th, 
  Td, 
  useColorModeValue,
  Icon,
  Divider
} from '@chakra-ui/react';
import { FaChartLine, FaShieldAlt, FaPercentage } from 'react-icons/fa';

const StakingRecommendation = ({ recommendation }) => {
  const cardBg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  const iconColor = useColorModeValue('near.primary', 'near.secondary');
  const progressTrackColor = useColorModeValue('gray.100', 'gray.700');

  // Determine risk color
  const getRiskColor = (risk) => {
    const riskMap = {
      'Low': 'green',
      'Medium': 'yellow',
      'High': 'orange',
      'Very High': 'red'
    };
    return riskMap[risk] || 'gray';
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
        <Icon as={FaShieldAlt} mr={3} color={iconColor} fontSize="xl" />
        <Heading as="h2" size="lg">Staking Recommendation</Heading>
      </Flex>

      <VStack spacing={6} align="stretch">
        <Box>
          <Text fontSize="md" mb={3} fontWeight="medium">
            {recommendation.summary}
          </Text>
        </Box>

        <Flex direction={["column", "row"]} gap={6} justifyContent="space-between">
          <Box flex="1">
            <Flex alignItems="center" mb={2}>
              <Icon as={FaPercentage} mr={2} color={iconColor} />
              <Text fontWeight="bold">Recommended Staking</Text>
            </Flex>
            <Progress 
              value={recommendation.stakingPercentage} 
              max={100} 
              colorScheme="blue" 
              height="24px"
              borderRadius="md"
              bg={progressTrackColor}
              mb={1}
            />
            <Flex justifyContent="space-between">
              <Text fontSize="sm" color="gray.500">0%</Text>
              <Text fontSize="md" fontWeight="bold">{recommendation.stakingPercentage}%</Text>
              <Text fontSize="sm" color="gray.500">100%</Text>
            </Flex>
          </Box>

          <Box flex="1">
            <Flex alignItems="center" mb={2}>
              <Icon as={FaChartLine} mr={2} color={iconColor} />
              <Text fontWeight="bold">Risk Assessment</Text>
            </Flex>
            <HStack spacing={4} mb={3}>
              <Badge colorScheme={getRiskColor(recommendation.riskLevel)} py={2} px={4} borderRadius="md" fontSize="md">
                {recommendation.riskLevel} Risk
              </Badge>
              <Text>Potential Monthly Yield: {recommendation.potentialMonthlyYield} NEAR</Text>
            </HStack>
            <Text fontSize="sm">{recommendation.riskMitigationStrategy}</Text>
          </Box>
        </Flex>

        <Divider my={3} />

        <Box>
          <Heading as="h3" size="md" mb={3}>Suggested Validators</Heading>
          <Table variant="simple" size="sm">
            <Thead>
              <Tr>
                <Th>Validator</Th>
                <Th isNumeric>APR (%)</Th>
                <Th isNumeric>Recommended Amount (NEAR)</Th>
              </Tr>
            </Thead>
            <Tbody>
              {recommendation.suggestedValidators.map((validator, index) => (
                <Tr key={index}>
                  <Td fontWeight="medium">{validator.name}</Td>
                  <Td isNumeric>{validator.apr}%</Td>
                  <Td isNumeric>{validator.recommendedAmount.toFixed(2)}</Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        </Box>
      </VStack>
    </Box>
  );
};

export default StakingRecommendation; 