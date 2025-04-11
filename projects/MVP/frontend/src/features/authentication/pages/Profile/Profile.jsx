import styles from "./Profile.module.css";
import { Box } from "../../components/Box/Box";
import { Button } from "../../../../components/Button/Button";
import { Input } from "../../../../components/Input/Input";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { useAuthentication } from "../../../authentication/contexts/AuthenticationContextProvider";


export function Profile() {

    const [step, setStep] = useState(0);
    const navigate = useNavigate();
    const { user, setUser } = useAuthentication();
    const [error, setError] = useState("");
    const [data, setData] = useState({
        firstName: user?.firstName || "",
        lastName: user?.lastName || "",
        company: user?.company || "",
        position: user?.position || "",
        location: user?.location || "",
    });

    const onSubmit = async () => {
      if (!data.firstName || !data.lastName) {
        setError("Please fill in your first and last name.");
        return;
      }
      if (!data.company || !data.position) {
        setError("Please fill in your latest company and position.");
        return;
      }
      if (!data.location) {
        setError("Please fill in your location.");
        return;
      }

      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/auth/profile/`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify({
            first_name: data.firstName,
            last_name: data.lastName,
            company: data.company,
            position: data.position,
            location: data.location,
          }),
        });
        if (response.ok) {
          const updatedUser = await response.json();
          setUser(updatedUser);
          navigate("/");
        } else {
          const { message } = await response.json();
          throw new Error(message);
        }
      } catch (error) {
        if (error instanceof TypeError) {
          setError(error.message);
        } else {
          setError("An error occurred. Please try again later.");
        }
      } finally {
        navigate("/");
      }
    };

    return (
        <div className={styles.root}>
          <Box>
            <h1>Only one last step</h1>
            <p>Tell us a bit about yourself so we can personalize your experience.</p>
            {step === 0 && (
              <div className={styles.inputs}>
                <Input
                  onFocus={() => setError("")}
                  required
                  label="First Name"
                  name="firstName"
                  placeholder="Jane"
                  onChange={(e) => setData((prev) => ({ ...prev, firstName: e.target.value }))}
                  value={data.firstName}
                ></Input>
                <Input
                  onFocus={() => setError("")}
                  required
                  label="Last Name"
                  name="lastName"
                  placeholder="Doe"
                  onChange={(e) => setData((prev) => ({ ...prev, lastName: e.target.value }))}
                  value={data.lastName}
                ></Input>
              </div>
            )}
            {step === 1 && (
              <div className={styles.inputs}>
                <Input
                  onFocus={() => setError("")}
                  label="Latest company"
                  name="company"
                  placeholder="Company name"
                  onChange={(e) => setData((prev) => ({ ...prev, company: e.target.value }))}
                  value={data.company}
                ></Input>
                <Input
                  onFocus={() => setError("")}
                  onChange={(e) => setData((prev) => ({ ...prev, position: e.target.value }))}
                  value={data.position}
                  label="Latest position"
                  name="position"
                  placeholder="Your role"
                ></Input>
              </div>
            )}
            {step == 2 && (
              <Input
                onFocus={() => setError("")}
                label="Location"
                name="location"
                placeholder="City, Country"
                value={data.location}
                onChange={(e) => setData((prev) => ({ ...prev, location: e.target.value }))}
              ></Input>
            )}
            {error && <p className={styles.error}>{error}</p>}
            <div className={styles.buttons}>
              {step > 0 && (
                <Button outline onClick={() => setStep((prev) => prev - 1)}>
                  Back
                </Button>
              )}
              {step < 2 && (
                <Button
                  disabled={
                    (step === 0 && (!data.firstName || !data.lastName)) ||
                    (step === 1 && (!data.company || !data.position))
                  }
                  onClick={() => setStep((prev) => prev + 1)}
                >
                  Next
                </Button>
              )}
              {step === 2 && (
                <Button disabled={!data.location} onClick={onSubmit}>
                  Submit
                </Button>
              )}
            </div>
          </Box>
        </div>
      );
}