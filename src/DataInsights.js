import React from 'react';
import { Box, Heading } from '@chakra-ui/react';

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
        <iframe
          src="/histogram_language.html"
          title="Language Distribution Histogram"
          width="100%"
          height="400px"
          style={{ border: 'none' }}
        />
      </Box>
      <Box my={5}>
        <Heading as="h3" size="lg" textAlign="center" mb={3}>
          Submission Times vs User ID
        </Heading>
        <iframe
          src="/scatter_submitted_at_vs_user_id.html"
          title="Submission Times vs User ID Scatter Plot"
          width="100%"
          height="400px"
          style={{ border: 'none' }}
        />
      </Box>
    </Box>
  );
};

export default DataInsights;
