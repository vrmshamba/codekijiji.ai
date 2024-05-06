import React from 'react';
import { Box, Heading, Text, List, ListItem } from '@chakra-ui/react';

const PartnershipPackages = () => {
  // Placeholder data for partnership packages
  const packages = [
    {
      name: 'Bronze',
      description: 'Basic partnership package offering standard features and support.',
      features: ['Feature 1', 'Feature 2', 'Feature 3']
    },
    {
      name: 'Silver',
      description: 'Enhanced partnership package with additional features and prioritized support.',
      features: ['Feature 1', 'Feature 2', 'Feature 3', 'Feature 4']
    },
    {
      name: 'Gold',
      description: 'Premium partnership package with all features, top-tier support, and strategic collaboration opportunities.',
      features: ['Feature 1', 'Feature 2', 'Feature 3', 'Feature 4', 'Feature 5']
    },
    {
      name: 'Platinum',
      description: 'Exclusive partnership package with bespoke features, dedicated support, and strategic collaboration opportunities.',
      features: ['Feature 1', 'Feature 2', 'Feature 3', 'Feature 4', 'Feature 5', 'Feature 6']
    }
  ];

  return (
    <Box>
      <Heading as="h1" size="xl" textAlign="center" my={5}>
        Partnership Packages
      </Heading>
      {packages.map((pkg) => (
        <Box key={pkg.name} p={5} shadow="md" borderWidth="1px" my={5}>
          <Heading as="h2" size="lg">{pkg.name}</Heading>
          <Text mt={4}>{pkg.description}</Text>
          <Heading as="h3" size="md" mt={4}>Features:</Heading>
          <List spacing={3}>
            {pkg.features.map((feature, index) => (
              <ListItem key={index}>{feature}</ListItem>
            ))}
          </List>
        </Box>
      ))}
    </Box>
  );
};

export default PartnershipPackages;
