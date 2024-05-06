import React from 'react';
import { Box, Image, Heading } from '@chakra-ui/react';

const DataInsights = () => {
  return (
    <Box>
      <Heading as="h2" size="xl" textAlign="center" my={5}>
        Data Visualizations
      </Heading>
      <Box my={5}>
        <Heading as="h3" size="lg" textAlign="center" mb={3}>
          Language Distribution
        </Heading>
        <Image src="/histogram_language.png" alt="Language Distribution Histogram" />
      </Box>
      <Box my={5}>
        <Heading as="h3" size="lg" textAlign="center" mb={3}>
          Submission Times vs User ID
        </Heading>
        <Image src="/scatter_submitted_at_vs_user_id.png" alt="Submission Times vs User ID Scatter Plot" />
      </Box>
    </Box>
  );
};

export default DataInsights;
