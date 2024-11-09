import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.Random;
import java.util.concurrent.TimeUnit;

public class FlakyTestSuiteObfuscated {

    @Test
    public void rbTest() {
        Random r = new Random();
        boolean p = r.nextBoolean();
        assertTrue(p, "Random test");
    }

    @Test
    public void tiTest() {
        long sT = System.currentTimeMillis();

        try {
            TimeUnit.MILLISECONDS.sleep(50);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        long eT = System.currentTimeMillis();
        long d = eT - sT;

        assertTrue(d < 40, "Timing test");
    }

    @Test
    public void ecTest() {
        String env = System.getenv("TE");

        assertEquals("staging", env, "Environment test");
    }

    @Test
    public void sbTest() {
        int res = add(2, 3);
        assertEquals(5, res, "Stable test");
    }

    private int add(int a, int b) {
        return a + b;
    }
}
