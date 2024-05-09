import React, { useState } from 'react';
import { Box, Heading, Tooltip, Spinner, useColorModeValue, Text } from '@chakra-ui/react';

const DataInsights = () => {
  const [loading, setLoading] = useState({ histogram: true, scatter: true });
  const [error, setError] = useState({ histogram: false, scatter: false });
  const boxBg = useColorModeValue('gray.50', 'gray.700');
  const headingColor = useColorModeValue('blue.600', 'blue.300');

  const handleIframeLoad = (visualization) => {
    setLoading((prevLoading) => ({ ...prevLoading, [visualization]: false }));
  };

  const handleIframeError = (visualization) => {
    setLoading((prevLoading) => ({ ...prevLoading, [visualization]: false }));
    setError((prevError) => ({ ...prevError, [visualization]: true }));
  };

  return (
    <Box bg={boxBg} p={5} borderRadius="lg" boxShadow="base">
      <Heading as="h2" size="xl" textAlign="center" my={5} color={headingColor}>
        Data Visualizations
      </Heading>
      <Box my={5} position="relative">
        <Tooltip label="Hover over the bars to see the language distribution counts" aria-label="Language distribution tooltip">
          <Heading as="h3" size="lg" textAlign="center" mb={3} color={headingColor}>
            Language Distribution
          </Heading>
          {loading.histogram && (
            <Spinner
              size="xl"
              position="absolute"
              left="50%"
              top="50%"
              transform="translate(-50%, -50%)"
            />
          )}
          {error.histogram && (
            <Text color="red.500" textAlign="center">
              Failed to load visualization. Please try again later.
            </Text>
          )}
          {!error.histogram && (
            <iframe
              src="/histogram_language.html"
              title="Language Distribution Histogram"
              width="100%"
              height="auto"
              style={{ border: 'none', paddingBottom: '56.25%', position: 'relative', height: 0 }}
              sandbox="allow-scripts allow-same-origin"
              aria-label="Interactive language distribution histogram"
              onLoad={() => handleIframeLoad('histogram')}
              onError={() => handleIframeError('histogram')}
            />
          )}
        </Tooltip>
      </Box>
      <Box my={5} position="relative">
        <Tooltip label="Drag to zoom, hover over points for more details" aria-label="Submission times tooltip">
          <Heading as="h3" size="lg" textAlign="center" mb={3} color={headingColor}>
            Submission Times vs User ID
          </Heading>
          {loading.scatter && (
            <Spinner
              size="xl"
              position="absolute"
              left="50%"
              top="50%"
              transform="translate(-50%, -50%)"
            />
          )}
          {error.scatter && (
            <Text color="red.500" textAlign="center">
              Failed to load visualization. Please try again later.
            </Text>
          )}
          {!error.scatter && (
            <iframe
              src="/scatter_submitted_at_vs_user_id.html"
              title="Submission Times vs User ID Scatter Plot"
              width="100%"
              height="auto"
              style={{ border: 'none', paddingBottom: '56.25%', position: 'relative', height: 0 }}
              sandbox="allow-scripts allow-same-origin"
              aria-label="Interactive scatter plot of submission times versus user IDs"
              onLoad={() => handleIframeLoad('scatter')}
              onError={() => handleIframeError('scatter')}
            />
          )}
        </Tooltip>
      </Box>
    </Box>
  );
};

export default DataInsights;
