import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.Random;
import java.util.concurrent.TimeUnit;

public class FlakyTestSuite {

    // Test with random behavior
    @Test
    public void testRandomBehavior() {
        Random random = new Random();
        boolean shouldPass = random.nextBoolean();
        assertTrue(shouldPass, "This test may randomly pass or fail.");
    }

    // Test with timing-related flakiness
    @Test
    public void testTimingIssue() {
        long startTime = System.currentTimeMillis();

        // Simulate processing delay
        try {
            TimeUnit.MILLISECONDS.sleep(50);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        long endTime = System.currentTimeMillis();
        long duration = endTime - startTime;

        // Expecting the operation to finish within 40ms
        assertTrue(duration < 40, "This test may fail if it takes too long.");
    }

    // Test dependent on an external condition (environment variable)
    @Test
    public void testExternalCondition() {
        String environment = System.getenv("TEST_ENV");

        // This test expects the environment variable "TEST_ENV" to be set to "staging"
        assertEquals("staging", environment, "This test may fail based on external conditions.");
    }

    @Test
    public void testStableBehavior() {
        int result = add(2, 3);
        assertEquals(5, result, "This test should always pass with consistent behavior.");
    }

    // A simple method for addition
    private int add(int a, int b) {
        return a + b;
    }
}
